import requests
from datetime import datetime


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
            print(f"Failed to authenticate guest. Status code: {response.status_code}")
            return None

    def fetch_product_ids(self, query):
        if not self.leshopch_token:
            print("No Leshopch token available")
            return []

        url = f"{self.base_url}/onesearch-oc-seaapi/public/v5/search"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Leshopch": self.leshopch_token
        }

        all_product_ids = []
        offset = 0
        limit = 100

        while True:
            payload = {
                "regionId": "national",
                "language": "de",
                "query": query,
                "sortFields": [],
                "sortOrder": "asc",
                "limit": limit,
                "offset": offset
            }
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                data = response.json()
                product_ids = data.get('productIds', [])
                all_product_ids.extend(product_ids)

                total_products = data.get('numberOfProducts', 0)

                if len(all_product_ids) >= total_products or len(product_ids) == 0:
                    break

                offset += limit
            else:
                print(f"Failed to fetch product IDs. Status code: {response.status_code}")
                break

        return all_product_ids

    def fetch_migros_ids(self, product_ids):
        if not self.leshopch_token:
            print("No Leshopch token available")
            return []

        url = f"{self.base_url}/product-display/public/v4/product-cards"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Leshopch": self.leshopch_token
        }

        all_migros_ids = []
        chunk_size = 100

        for i in range(0, len(product_ids), chunk_size):
            chunk = product_ids[i:i + chunk_size]
            payload = {
                "offerFilter": {
                    "storeType": "OFFLINE",
                    "region": "national",
                    "ongoingOfferDate": datetime.now().strftime("%Y-%m-%dT00:00:00")
                },
                "productFilter": {
                    "uids": chunk
                }
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                products = response.json()
                migros_ids = [product['migrosId'] for product in products if 'migrosId' in product]
                all_migros_ids.extend(migros_ids)
            else:
                print(
                    f"Failed to fetch Migros IDs for chunk {i // chunk_size + 1}. Status code: {response.status_code}")

        print(f"Fetched a total of {len(all_migros_ids)} Migros IDs out of {len(product_ids)} product IDs")
        return all_migros_ids
