from typing import List, Dict, Any
from app.services.job_source import JobSource


# Exemple d'implémentation pour France Travail (à compléter en Phase 3)
class FranceTravailSource(JobSource):
    """Source d'offres d'emploi via l'API France Travail."""

    @property
    def name(self) -> str:
        return "France Travail"

    async def search_offers(self, keywords: List[str], location: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        # TODO: Implémenter la connexion à l'API France Travail
        return []

    async def get_offer_details(self, offer_id: str) -> Dict[str, Any]:
        # TODO: Implémenter la récupération des détails d'une offre
        return {}
