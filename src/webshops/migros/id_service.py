import requests

class MigrosIDService:
    def __init__(self, base_url):
        self.base_url = base_url
        self.leshopch_token = self.authenticate_guest()

    def authenticate_guest(self):
        url = f"{self.base_url}/authentication/public/v1/api/guest?authorizationNotRequired=true"
        response = requests.get(url)
        if response.status_code == 200:
            return response.headers.get('Leshopch')
        else:
            return None

    def fetch_product_ids(self, query):
        if not self.leshopch_token:
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
            "limit": 1
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get('productIds', [])
        else:
            return []

    def fetch_migros_ids(self, product_ids):
        if not self.leshopch_token:
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
        if response.status_code == 200:
            products = response.json()
            return [product['migrosId'] for product in products if 'migrosId' in product]
        else:
            return []
