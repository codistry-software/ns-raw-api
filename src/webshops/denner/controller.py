from .id_service import DennerIDService

class DennerController:
    def __init__(self):
        self.base_url = "https://www.denner.ch"
        self.id_service = DennerIDService(self.base_url)
        self.processed_urls = set()

    def process_query(self, query):
        all_product_urls = self.id_service.fetch_all_product_urls()
        results = []

        for url in all_product_urls:
            if url not in self.processed_urls:
                details = self.fetch_product_details(url)
                if details:
                    results.append(details)
                    self.processed_urls.add(url)
            else:
                print(f"Skipping duplicate product URL: {url}")

        return results

    def fetch_product_details(self, url):
        return {"url": url}
