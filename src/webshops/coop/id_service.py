import requests

class CoopIDService:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,de-CH;q=0.7,de;q=0.6',
            'Referer': 'https://www.coop.ch/de'
        }
        self.init_session()

    def init_session(self):
        homepage_response = self.session.get(f"{self.base_url}/de", headers=self.headers)
        if homepage_response.status_code != 200:
            print("Failed to initialize session")
        else:
            print("Session initialized with cookies:", self.session.cookies.get_dict())

    def search_products(self, query):
        url = f"{self.base_url}/de/dynamic-pageload/searchresultJson?componentName=searchresultJson&url={self.base_url}/de/search/?text={query}&displayUrl={self.base_url}/de/search/?text={query}&compiledTemplates[]=productTile&compiledTemplates[]=sellingBanner"
        response = self.session.get(url, headers=self.headers)
        if response.status_code == 200:
            try:
                product_data = response.json()
                # Ensuring the existence of the expected data structure
                content_jsons = product_data.get('contentJsons', {})
                anchors = content_jsons.get('anchors', [])
                if anchors and len(anchors) > 1:
                    elements = anchors[1].get('json', {}).get('elements', [])
                    product_ids = [element['id'] for element in elements]
                    return product_ids
                else:
                    print("No products found or unexpected JSON structure.")
                    return []
            except KeyError:
                print("KeyError: The JSON response does not have the expected format.")
                return []
        else:
            print(f"Failed to retrieve product IDs with status code: {response.status_code}")
            return []
