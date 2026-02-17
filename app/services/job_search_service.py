from typing import List, Dict, Any
from app.services.job_source import JobSource


class JobSearchService:
    """
    Service central de recherche d'offres.
    Il agrège les résultats de toutes les sources enregistrées.
    Pour ajouter une nouvelle source, il suffit de l'enregistrer avec add_source().
    """

    def __init__(self):
        self._sources: List[JobSource] = []

    def add_source(self, source: JobSource):
        """Ajouter une nouvelle source d'offres d'emploi."""
        self._sources.append(source)
        print(f"Source ajoutée : {source.name}")

    def list_sources(self) -> List[str]:
        """Lister toutes les sources enregistrées."""
        return [source.name for source in self._sources]

    async def search_all(self, keywords: List[str], location: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        """
        Rechercher des offres sur TOUTES les sources enregistrées.
        Les résultats sont fusionnés et retournés dans une seule liste.
        """
        all_offers = []

        for source in self._sources:
            try:
                offers = await source.search_offers(keywords, location, limit)
                all_offers.extend(offers)
            except Exception as e:
                print(f"Erreur avec la source {source.name}: {e}")

        return all_offers
