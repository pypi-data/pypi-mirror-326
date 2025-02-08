class InternetSearch:
    """Search for up-to-date information on the internet"""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def search(self, natural_language_query: str) -> str:
        """
        Search for up-to-date information on the internet and return result in markdown format.

        Args:
            natural_language_query (str): A query string that matches a specific topic, concept, or fact.
              It should be formulated in natural language and be as specific as possible.
        """
        from freeact_skills.search.google import impl

        return impl.search(natural_language_query, self.api_key)
