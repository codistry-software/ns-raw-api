import requests
from bs4 import BeautifulSoup
import re

class DennerIDService:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_product_urls(self, page=1):
        if page == 1:
            url = f"{self.base_url}/de/suche/"
            params = {
                'L': '0',
                'id': '19',
                'tx_solr[q]': '*'
            }
        else:
            url = f"{self.base_url}/de/suche/"
            params = {
                'tx_solr[page]': str(page),
                'tx_solr[q]': '*'
            }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, params=params, headers=headers)
        print(f"Request URL: {response.url}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_info = []

            results_found = soup.select_one('.result-found')
            total_results = 0
            if results_found:
                match = re.search(r'\d+', results_found.text)
                if match:
                    total_results = int(match.group())

            search_results = soup.select('.search-result')

            for item in search_results:
                category_section = item.select_one('.results-teaser')
                if category_section:
                    category_text = category_section.get_text(strip=True)
                    category_match = re.search(r'Bereiche\s*(.*)', category_text)
                    if category_match:
                        category = category_match.group(1).strip()
                        if 'Produkte' in category or 'Wein Shop' in category:
                            url_element = item.select_one('.results-topic a')
                            if url_element and 'href' in url_element.attrs:
                                url = url_element['href']
                                full_url = self.base_url + url
                                product_name = url_element.text.strip()
                                product_info.append((product_name, full_url))

            return product_info, total_results
        else:
            print(f"Failed to fetch product URLs. Status code: {response.status_code}")
            return [], 0
