from webshops.migros.id_service import MigrosIDService
from webshops.migros.product_service import MigrosProductService

class MigrosController:
    def __init__(self):
        self.base_url = "https://www.migros.ch"
        self.id_service = MigrosIDService(self.base_url)
        self.product_service = MigrosProductService(self.base_url, self.id_service.leshopch_token)
        self.processed_ids = set()

    def fetch_product_ids(self, query):
        return self.id_service.fetch_product_ids(query)

    def fetch_migros_ids(self, product_ids):
        return self.id_service.fetch_migros_ids(product_ids)

    def fetch_product_details(self, migros_id):
        return self.product_service.fetch_product_details(migros_id)

    def process_query(self, query):
        product_ids = self.fetch_product_ids(query)
        migros_ids = self.fetch_migros_ids(product_ids)
        results = []
        for migros_id in migros_ids:
            if migros_id not in self.processed_ids:
                details = self.fetch_product_details(migros_id)
                if details:
                    results.append(details)
                    self.processed_ids.add(migros_id)
            else:
                print(f"Skipping duplicate product with Migros ID: {migros_id}")
        return results
