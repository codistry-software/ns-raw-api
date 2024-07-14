import requests

class CoopIDService:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_product_ids(self, query):
        # Prepare the URL with the query included
        url = f"{self.base_url}/de/dynamic-pageload/searchresultJson?componentName=searchresultJson&url={self.base_url}/de/search/?text={query}&displayUrl={self.base_url}/de/search/?text={query}&compiledTemplates[]=productTile&compiledTemplates[]=sellingBanner"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,de-CH;q=0.7,de;q=0.6",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
        }

        # Send the request
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Extract product IDs from the JSON response
            product_data = response.json()
            product_ids = [element['id'] for element in product_data['contentJsons']['anchors'][1]['json']['elements']]
            return product_ids
        else:
            print(f"Failed to retrieve product IDs: {response.status_code}")
            return []
