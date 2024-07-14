from webshops.coop.id_service import CoopIDService

class CoopController:
    def __init__(self):
        self.base_url = "https://www.coop.ch"
        self.id_service = CoopIDService(self.base_url)

    def process_query(self, query):
        product_ids = self.id_service.search_products(query)
        if product_ids:
            print(f"Found product IDs for '{query}': {product_ids}")
        else:
            print(f"No products found for: {query}")
        return product_ids
