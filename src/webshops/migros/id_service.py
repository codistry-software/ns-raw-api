import requests
from src.logger.logger import logger

class MigrosIDService:
    def __init__(self, base_url):
        self.base_url = base_url
        self.leshopch_token = self.authenticate_guest()

    def authenticate_guest(self):
        url = f"{self.base_url}/authentication/public/v1/api/guest?authorizationNotRequired=true"
        response = requests.get(url)
        if response.status_code == 200:
            leshopch_token = response.headers.get('Leshopch')
            logger.info(f"Authenticated, Leshopch Token: {leshopch_token}")
            return leshopch_token
        else:
            logger.error(f"Failed to authenticate: {response.status_code}")
            return None

    def fetch_product_ids(self, query):
        if not self.leshopch_token:
            logger.error("Authentication failed, cannot fetch product IDs.")
            return []

        url = f"{self.base_url}/onesearch-oc-seaapi/public/v5/search"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Leshopch": self.leshopch_token
        }
        payload = {
            "regionId": "national",
            "language": "de",
            "query": query,
            "sortFields": [],
            "sortOrder": "asc",
            "limit": 12
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            product_ids = response.json().get('productIds', [])
            logger.info(f"Product IDs: {product_ids}")
            return product_ids
        else:
            logger.error(f"Failed to fetch data: {response.status_code}, {response.text}")
            return []

    def fetch_migros_ids(self, product_ids):
        if not self.leshopch_token:
            logger.error("Authentication failed, cannot fetch Migros IDs.")
            return []

        url = f"{self.base_url}/product-display/public/v4/product-cards"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Leshopch": self.leshopch_token
        }
        payload = {
            "offerFilter": {
                "storeType": "OFFLINE",
                "region": "national",
                "ongoingOfferDate": "2024-07-13T00:00:00"
            },
            "productFilter": {
                "uids": product_ids
            }
        }

        response = requests.post(url, json=payload, headers=headers)
        logger.debug(f"Response Status Code: {response.status_code}")
        if response.status_code == 200:
            products = response.json()
            migros_ids = [product['migrosId'] for product in products if 'migrosId' in product]
            logger.info(f"Migros IDs: {migros_ids}")
            return migros_ids
        else:
            logger.error(f"Failed to fetch Migros IDs: {response.status_code}, {response.text}")
            return []
