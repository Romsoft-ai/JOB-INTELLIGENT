import os
import sys
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from pathlib import Path
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.services.job_source import JobSource

# Charger les variables d'environnement
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

FRANCE_TRAVAIL_CLIENT_ID = os.getenv('FRANCE_TRAVAIL_CLIENT_ID')
FRANCE_TRAVAIL_CLIENT_SECRET = os.getenv('FRANCE_TRAVAIL_CLIENT_SECRET')

# URLs France Travail (nouveaux endpoints)
TOKEN_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"
OFFRES_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
SCOPE = "api_offresdemploiv2 o2dsoffre"
SLEEP_BETWEEN_REQUESTS_S = 0.2
MAX_PER_REQUEST = 150

class FranceTravailAPI:
    def __init__(self):
        self.token = self.get_access_token()

    def get_access_token(self):
        data = {
            'grant_type': 'client_credentials',
            'client_id': FRANCE_TRAVAIL_CLIENT_ID,
            'client_secret': FRANCE_TRAVAIL_CLIENT_SECRET,
            'scope': SCOPE
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(TOKEN_URL, data=data, headers=headers, timeout=30)
        print(f"[INFO] Token status: {response.status_code}")
        if response.status_code != 200:
            print(f"[ERROR] Token response: {response.text}")
        response.raise_for_status()
        token_data = response.json()
        print(f"[INFO] scope: {token_data.get('scope')}, expires_in: {token_data.get('expires_in')}s")
        return token_data['access_token']

    def fetch_page(self, mots_cles: str, start: int, end: int) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "User-Agent": "JOB-Intelligent/1.0 (school project)",
        }
        params = {
            "motsCles": mots_cles,
            "range": f"{start}-{end}",
        }
        r = requests.get(OFFRES_URL, headers=headers, params=params, timeout=30)
        if r.status_code not in (200, 206):
            print(f"[ERROR] Search status: {r.status_code}")
            print(f"[ERROR] Search headers: {dict(r.headers)}")
            print(f"[ERROR] Search body: {r.text[:800]}")
        r.raise_for_status()
        return r.json(), dict(r.headers)

    def collect_all_offers(self, mots_cles: str, batch_size: int = MAX_PER_REQUEST) -> List[Dict[str, Any]]:
        print("\n[STEP 2] Collecte des offres (pagination) ...")
        print(f"[INFO] Query: motsCles='{mots_cles}' | batch_size={batch_size}")
        first_json, first_headers = self.fetch_page(mots_cles, 0, batch_size - 1)
        content_range = first_headers.get("Content-Range", "")
        print(f"[INFO] Content-Range: {content_range}")
        total = None
        if "/" in content_range:
            try:
                total = int(content_range.split("/")[-1])
            except Exception:
                total = None
        results = list(first_json.get("resultats", []))
        if total is None:
            total = len(results)
        print(f"[INFO] Total annoncé: {total} | récupéré (page 1): {len(results)}")
        # Limite API France Travail : start <= 3000
        max_api_index = 3000
        for start in range(batch_size, min(total, max_api_index + 1), batch_size):
            end = max(start, min(start + batch_size - 1, min(total, max_api_index) - 1))
            if end < start:
                break
            page_json, _ = self.fetch_page(mots_cles, start, end)
            page_res = page_json.get("resultats", [])
            results.extend(page_res)
            print(f"[INFO] Page {start}-{end} | +{len(page_res)} offres | cumul={len(results)}")
            time.sleep(SLEEP_BETWEEN_REQUESTS_S)
        print(f"[OK] Collecte terminée. Total récupéré: {len(results)}")
        return results

def get_nested(d: dict, path: str, default=None):
    cur = d
    for key in path.split('.'):
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur

def clean_offer(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Nettoie une offre brute et renomme les champs pour plus de clarté."""
    return {
        "id": raw.get("id"),
        "titre": raw.get("intitule"),
        "description": raw.get("description"),
        "date_actualisation": raw.get("dateActualisation"),
        "ville": get_nested(raw, "lieuTravail.libelle"),
        "code_postal": get_nested(raw, "lieuTravail.codePostal"),
        "rome_code": raw.get("romeCode"),
        "rome_libelle": raw.get("romeLibelle"),
        "nom_entreprise": get_nested(raw, "entreprise.nom"),
        "type_contrat": raw.get("typeContrat"),
        "nature_contrat": raw.get("natureContrat"),
        "experience": raw.get("experienceLibelle"),
        "salaire": get_nested(raw, "salaire.libelle"),
        "contact_nom": get_nested(raw, "contact.nom"),
        "contact_tel": get_nested(raw, "contact.coordonnees1"),
        "contact_email": get_nested(raw, "contact.courriel"),
        "nombre_postes": raw.get("nombrePostes"),
        "qualification": raw.get("qualificationLibelle"),
        "secteur_activite": raw.get("secteurActiviteLibelle"),
        "effectif_etablissement": raw.get("trancheEffectifEtab"),
        "url_origine": get_nested(raw, "origineOffre.urlOrigine"),
    }

class FranceTravailSource(JobSource):
    """Source d'offres d'emploi via l'API France Travail."""

    @property
    def name(self) -> str:
        return "France Travail"

    async def search_offers(self, keywords: List[str], location: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        # Recherche des offres avec les mots-clés donnés par l'utilisateur
        mots_cles = " ".join(keywords)
        api = FranceTravailAPI()
        offres = api.collect_all_offers(mots_cles=mots_cles, batch_size=limit)
        # Nettoyage
        cleaned_offres = [clean_offer(o) for o in offres]
        # Sauvegarde dans data/offres_{mots_cles}_{date}.json
        from datetime import datetime
        import json
        from pathlib import Path
        today = datetime.now().strftime("%Y-%m-%d")
        # Formatage du nom de fichier (remplace espaces par _)
        safe_mots_cles = mots_cles.replace(" ", "_").replace(",", "_")
        output_path = Path("data") / f"offres_{safe_mots_cles}_{today}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(cleaned_offres, f, ensure_ascii=False, indent=2)
        return cleaned_offres[:limit]

    async def get_offer_details(self, offer_id: str) -> Dict[str, Any]:
        # TODO: Implémenter la récupération des détails d'une offre
        return {}

if __name__ == "__main__":
    from datetime import datetime
    import json
    from pathlib import Path

    api = FranceTravailAPI()
    offres = api.collect_all_offers(mots_cles="data analyst", batch_size=150)
    print(f"Nombre d'offres récupérées: {len(offres)}")
    # Nettoyage des offres
    cleaned_offres = [clean_offer(o) for o in offres]
    # Sauvegarde dans data/{date}.json
    today = datetime.now().strftime("%Y-%m-%d")
    output_path = Path("data") / f"{today}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_offres, f, ensure_ascii=False, indent=2)
    print(f"Offres nettoyées sauvegardées dans : {output_path}")
