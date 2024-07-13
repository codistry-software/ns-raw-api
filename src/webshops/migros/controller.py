from webshops.migros.id_service import MigrosIDService
from webshops.migros.product_service import MigrosProductService
from src.logger.logger import logger

class MigrosController:
    def __init__(self):
        self.base_url = "https://www.migros.ch"
        self.id_service = MigrosIDService(self.base_url)
        self.product_service = MigrosProductService(self.base_url, self.id_service.leshopch_token)

    def fetch_product_ids(self, query):
        return self.id_service.fetch_product_ids(query)

    def fetch_migros_ids(self, product_ids):
        return self.id_service.fetch_migros_ids(product_ids)

    def fetch_product_details(self, migros_id):
        return self.product_service.fetch_product_details(migros_id)
