import requests
from src.logger.logger import logger

class MigrosProductService:
    def __init__(self, base_url, leshopch_token):
        self.base_url = base_url
        self.leshopch_token = leshopch_token

    def fetch_product_details(self, migros_id):
        url = f"{self.base_url}/product-display/public/v2/product-detail"
        params = {
            "storeType": "OFFLINE",
            "warehouseId": 2,
            "region": "national",
            "ongoingOfferDate": "2024-07-13T00:00:00",
            "migrosIds": migros_id
        }
        headers = {
            "Accept": "application/json",
            "Leshopch": self.leshopch_token
        }

        response = requests.get(url, headers=headers, params=params)
        logger.debug(f"Response Status Code: {response.status_code}")
        if response.status_code == 200:
            response_json = response.json()
            logger.debug(f"Response JSON: {response_json}")
            return self.parse_product_data(response_json)
        else:
            logger.error(f"Failed to fetch product data: {response.status_code}, {response.text}")
            return None

    def parse_product_data(self, data):
        if not data:
            logger.warning("No product data found")
            return None

        product = data[0]
        product_info = {
            "Name": product.get("name"),
            "Price": product["offer"]["price"].get("formattedPrice", "N/A"),
            "Weight": product["offer"].get("quantity", "N/A"),
            "Nutrients": {row["label"]: row["values"][0] for row in product["productInformation"]["nutrientsInformation"]["nutrientsTable"]["rows"]},
            "Ingredients": product["productInformation"]["mainInformation"].get("ingredients", "N/A"),
            "Sale": "Yes" if product['offer'].get('isNewOffer', False) else "No",
            "Category": [breadcrumb["name"] for breadcrumb in product["breadcrumb"]]
        }
        return product_info
