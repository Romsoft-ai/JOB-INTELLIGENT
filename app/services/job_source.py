from abc import ABC, abstractmethod
from typing import List, Dict, Any


class JobSource(ABC):
    """
    Classe abstraite (interface) pour les sources d'offres d'emploi.
    Chaque nouvelle source (France Travail, Indeed, LinkedIn, etc.)
    doit hériter de cette classe et implémenter ses méthodes.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Nom de la source (ex: 'France Travail', 'Indeed')."""
        pass

    @abstractmethod
    async def search_offers(self, keywords: List[str], location: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        """
        Rechercher des offres d'emploi.

        Args:
            keywords: Liste de mots-clés (compétences, métier, etc.)
            location: Localisation souhaitée (ville, département, etc.)
            limit: Nombre maximum d'offres à retourner

        Returns:
            Liste de dictionnaires contenant les offres trouvées.
            Chaque offre doit contenir au minimum :
                - title: str (titre du poste)
                - company: str (nom de l'entreprise)
                - location: str (lieu)
                - description: str (description de l'offre)
                - url: str (lien pour postuler)
                - source: str (nom de la source)
        """
        pass

    @abstractmethod
    async def get_offer_details(self, offer_id: str) -> Dict[str, Any]:
        """
        Récupérer les détails d'une offre spécifique.

        Args:
            offer_id: Identifiant unique de l'offre

        Returns:
            Dictionnaire contenant les détails complets de l'offre.
        """
        pass
