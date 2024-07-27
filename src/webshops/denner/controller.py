from .id_service import DennerIDService
from .product_service import DennerProductService
import json


class DennerController:
    def __init__(self):
        self.base_url = "https://www.denner.ch"
        self.id_service = DennerIDService(self.base_url)
        self.product_service = DennerProductService()
        self.processed_urls = set()

    def process_query(self, query):
        results = []
        page = 1

        while True:
            product_info, total_results = self.id_service.fetch_product_urls(page)

            if not product_info:
                break

            print(f"\nProcessing page {page}")
            print(f"Fetched {len(product_info)} products. Total: {len(self.processed_urls)}/{total_results}")

            for product_name, url in product_info:
                if url not in self.processed_urls:
                    details = self.product_service.fetch_product_details(url)
                    if details:
                        results.append(details)
                        self.processed_urls.add(url)
                        print(f"\nProduct Details for {url}:")
                        print(json.dumps(details, indent=2, ensure_ascii=False))
                else:
                    print(f"Skipping duplicate product URL: {url}")

            if len(self.processed_urls) >= total_results:
                break

            page += 1

        return results
