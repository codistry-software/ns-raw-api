from webshops.coop.id_service import CoopIDService

class CoopController:
    def __init__(self):
        self.base_url = "https://www.coop.ch"
        self.id_service = CoopIDService(self.base_url)

    def process_all_pages(self, query='all'):
        page = 1
        while True:
            product_ids = self.id_service.search_products_by_page(query, page)
            if product_ids:
                print(f"Page {page}: Found product IDs: {product_ids}")
                page += 1
            else:
                print(f"Page {page}: No more products found or error occurred.")
                break
