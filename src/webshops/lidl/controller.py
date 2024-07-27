import json
from .id_service import LidlIDService
from .product_service import LidlProductService


class LidlController:
    def __init__(self):
        self.base_url = "https://sortiment.lidl.ch"
        self.id_service = LidlIDService(self.base_url)
        self.product_service = LidlProductService()
        self.processed_urls = set()

    def process_query(self, query):
        results = []
        page = 1

        while True:
            product_urls = self.id_service.fetch_product_urls(page)
            if not product_urls:
                break

            print(f"Processing page {page}")
            for url in product_urls:
                if url not in self.processed_urls:
                    details = self.product_service.fetch_product_details(url)
                    if details:
                        results.append(details)
                        self.processed_urls.add(url)
                        print(f"Product Details:\n{json.dumps(details, indent=2, ensure_ascii=False)}")
                else:
                    print(f"Skipping duplicate product URL: {url}")

            page += 1

        return results
