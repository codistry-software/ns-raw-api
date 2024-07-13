import requests

class MigrosProductService:
    def __init__(self, base_url, leshopch_token):
        self.base_url = base_url
        self.leshopch_token = leshopch_token
        self.non_food_categories = {
            "Drogerie & Kosmetik",
            "Waschen & Putzen",
            "Baby & Kinder",
            "Tierbedarf",
            "Haushalt & Wohnen",
            "Bekleidung & Accessoires"
        }

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
        if response.status_code == 200:
            data = response.json()
            return self.parse_product_data(data)
        else:
            return None

    def is_food_product(self, product):
        breadcrumbs = product.get('breadcrumb', [])
        if breadcrumbs and breadcrumbs[0].get('name') in self.non_food_categories:
            return False
        return True

    def parse_product_data(self, data):
        if not data:
            return None

        product = data[0]

        if not self.is_food_product(product):
            print(f"Überspringe Nicht-Lebensmittel: {product.get('title')}")
            return None

        is_on_sale = 'badges' in product['offer'] and any(badge['type'] == 'PERCENTAGE_PROMOTION' for badge in product['offer']['badges'])
        sale_percentage = next((badge['description'] for badge in product['offer']['badges'] if badge['type'] == 'PERCENTAGE_PROMOTION'), "No sale") if is_on_sale else "No sale"

        nutrients_info = product.get("productInformation", {}).get("nutrientsInformation", {}).get("nutrientsTable", {}).get("rows", [])
        nutrients = {row["label"]: row["values"][0] for row in nutrients_info} if nutrients_info else {}

        title = product.get("title", "").replace(".", "")

        product_info = {
            "Name": title,
            "Price": product["offer"]["price"].get("formattedPrice", "N/A"),
            "Weight": product["offer"].get("quantity", "N/A"),
            "Nutrients": nutrients,
            "Ingredients": product["productInformation"]["mainInformation"].get("ingredients", "N/A"),
            "Sale": is_on_sale,
            "Sale Percentage": sale_percentage,
            "Category": [breadcrumb.get("name", "N/A") for breadcrumb in product.get("breadcrumb", [])]
        }

        return product_info