import os
import json
from google.cloud import bigquery

# === CONFIGURATION ===
GCP_KEY_PATH = "bq-uploader-key.json"  # Chemin vers la clé de service
PROJECT_ID = "job-intelligent-rec"      # Remplace par l'ID de ton projet GCP
DATASET_ID = "Job_offers"              # Nom du dataset BigQuery
TABLE_ID = "offres_france_travail"     # Nom de la table
JSON_PATH = "data/2026-02-18.json"     # Fichier à uploader

# === AUTHENTIFICATION ===
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GCP_KEY_PATH

# === SCHÉMA BIGQUERY ===
SCHEMA = [
    bigquery.SchemaField("id", "STRING"),
    bigquery.SchemaField("titre", "STRING"),
    bigquery.SchemaField("description", "STRING"),
    bigquery.SchemaField("date_actualisation", "TIMESTAMP"),
    bigquery.SchemaField("ville", "STRING"),
    bigquery.SchemaField("code_postal", "STRING"),
    bigquery.SchemaField("rome_code", "STRING"),
    bigquery.SchemaField("rome_libelle", "STRING"),
    bigquery.SchemaField("nom_entreprise", "STRING"),
    bigquery.SchemaField("type_contrat", "STRING"),
    bigquery.SchemaField("nature_contrat", "STRING"),
    bigquery.SchemaField("experience", "STRING"),
    bigquery.SchemaField("salaire", "STRING"),
    bigquery.SchemaField("contact_nom", "STRING"),
    bigquery.SchemaField("contact_tel", "STRING"),
    bigquery.SchemaField("contact_email", "STRING"),
    bigquery.SchemaField("nombre_postes", "INTEGER"),
    bigquery.SchemaField("qualification", "STRING"),
    bigquery.SchemaField("secteur_activite", "STRING"),
    bigquery.SchemaField("effectif_etablissement", "STRING"),
    bigquery.SchemaField("url_origine", "STRING"),
]

# === UPLOAD ===
def upload_json_to_bigquery():
    client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    # Crée la table si elle n'existe pas
    try:
        client.get_table(table_ref)
        print("Table déjà existante.")
    except Exception:
        table = bigquery.Table(table_ref, schema=SCHEMA)
        client.create_table(table)
        print("Table créée.")

    # Charge les données JSON
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        rows = json.load(f)

    # Nettoie les lignes vides ou incomplètes
    rows = [row for row in rows if row.get("id")]

    # Récupère les IDs déjà présents dans la table
    query = f"SELECT id FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` WHERE id IS NOT NULL"
    existing_ids = set()
    try:
        query_job = client.query(query)
        for row in query_job:
            existing_ids.add(row["id"])
    except Exception as e:
        print("Erreur lors de la récupération des IDs existants :", e)

    # Filtre les nouvelles offres (id non déjà présent)
    new_rows = [row for row in rows if row["id"] not in existing_ids]
    print(f"{len(new_rows)} nouvelles offres à insérer (sur {len(rows)} offres totales dans le JSON)")

    if not new_rows:
        print("Aucune nouvelle offre à insérer.")
        return

    # Insertion
    errors = client.insert_rows_json(table_ref, new_rows)
    if errors:
        print("Erreurs lors de l'insertion :", errors)
    else:
        print(f"{len(new_rows)} nouvelles lignes insérées dans {table_ref}")

if __name__ == "__main__":
    upload_json_to_bigquery()