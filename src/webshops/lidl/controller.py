from .id_service import LidlIDService

class LidlController:
    def __init__(self):
        self.base_url = "https://sortiment.lidl.ch"
        self.id_service = LidlIDService(self.base_url)
        self.processed_urls = set()

    def process_query(self, query):
        # Ignore the query parameter for Lidl as we're fetching all products
        all_product_urls = self.id_service.fetch_all_product_urls()
        results = []

        for url in all_product_urls:
            if url not in self.processed_urls:
                details = self.fetch_product_details(url)
                if details:
                    results.append(details)
                    self.processed_urls.add(url)
                    print(f"Processed product: {url}")
            else:
                print(f"Skipping duplicate product URL: {url}")

        return results

    def fetch_product_details(self, url):
        return {"url": url, "name": self.extract_product_name(url)}

    def extract_product_name(self, url):
        return url.split('/')[-1].replace('-', ' ').title()
