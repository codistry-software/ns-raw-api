import requests


class CoopIDService:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
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

    def is_valid_path(self, path):
        excluded_prefixes = [
            "https://www.coop.ch/de/haushalt-tier",
            "https://www.coop.ch/de/kosmetik-gesundheit"
        ]
        included_prefixes = [
            "https://www.coop.ch/de/baby-kind/babynahrung",
            "https://www.coop.ch/de/baby-kind/milchpulver"
        ]

        if any(path.startswith(prefix) for prefix in excluded_prefixes):
            return False

        if path.startswith("https://www.coop.ch/de/baby-kind"):
            return any(path.startswith(prefix) for prefix in included_prefixes)

        return True

    def search_products_by_page(self, query='all', page=1):
        url = f"{self.base_url}/de/dynamic-pageload/searchresultJson?componentName=searchresultJson&url=https%3A%2F%2Fwww.coop.ch%2Fde%2Fsearch%3Fpage%3D{page}%26pageSize%3D30%26q%3D{query}%253Arelevance%26text%3D{query}%26sort%3Drelevance&displayUrl=https%3A%2F%2Fwww.coop.ch%2Fde%2Fsearch%3Fpage%3D{page}%26pageSize%3D30%26q%3D{query}%253Arelevance%26text%3D{query}%26sort%3Drelevance&compiledTemplates%5B%5D=productTile&compiledTemplates%5B%5D=sellingBanner"
        response = self.session.get(url, headers=self.headers)
        if response.status_code == 200:
            try:
                product_data = response.json()
                content_jsons = product_data.get('contentJsons', {})
                if content_jsons:
                    paths = []
                    for anchor in content_jsons.get('anchors', []):
                        if anchor.get('name') == 'productTile':
                            elements = anchor.get('json', {}).get('elements', [])
                            for element in elements:
                                href = element.get('href')
                                if href:
                                    full_path = f"https://www.coop.ch{href}?context=search"
                                    if self.is_valid_path(full_path):
                                        paths.append(full_path)
                    return paths
                print("No products found or unexpected JSON structure.")
            except ValueError as e:
                print(f"JSON decoding failed: {e}")
            except KeyError:
                print("KeyError: The JSON response does not have the expected format.")
        else:
            print(f"Failed to retrieve product paths with status code: {response.status_code}")
        return []

    def search_all_products(self, query='all'):
        page = 1
        all_product_paths = []
        while True:
            product_paths = self.search_products_by_page(query, page)
            if product_paths:
                all_product_paths.extend(product_paths)
                page += 1
            else:
                break
        return all_product_paths
