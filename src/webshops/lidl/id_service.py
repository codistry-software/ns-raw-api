import requests
from bs4 import BeautifulSoup


class LidlIDService:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_product_urls(self, page=1):
        url = f"{self.base_url}/de/alle-kategorien"
        params = {'p': str(page)}

        response = requests.get(url, params=params, headers=self.headers)
        print(f"Request URL: {response.url}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_urls = []

            products = soup.select('li.item.product.product-item')
            for product in products:
                product_link = product.select_one('a.product-item-link')
                if product_link and 'href' in product_link.attrs:
                    product_url = product_link['href']
                    product_urls.append(product_url)
                    print(f"Product URL: {product_url}")

            return product_urls
        else:
            print(f"Failed to fetch product URLs. Status code: {response.status_code}")
            return []

    def fetch_all_product_urls(self):
        all_product_urls = []
        page = 1

        while True:
            product_urls = self.fetch_product_urls(page)
            if not product_urls:
                break

            all_product_urls.extend(product_urls)
            print(f"Page {page}: Fetched {len(product_urls)} products. Total: {len(all_product_urls)}")
            page += 1

        return all_product_urls
