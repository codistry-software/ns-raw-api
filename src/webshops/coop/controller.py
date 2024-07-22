from webshops.coop.id_service import CoopIDService
from webshops.coop.product_service import CoopProductService

class CoopController:
    def __init__(self):
        self.base_url = "https://www.coop.ch"
        self.id_service = CoopIDService(self.base_url)
        self.product_service = CoopProductService(self.id_service.session)

    def process_all_pages(self, query='all'):
        page = 1
        while True:
            product_paths = self.id_service.search_products_by_page(query, page)
            if product_paths:
                print(f"Page {page}: Found product paths: {product_paths}")
                for path in product_paths:
                    product_details = self.product_service.fetch_product_details(path)
                    print(product_details)
                page += 1
            else:
                print(f"Page {page}: No more products found or error occurred.")
                break
