import requests
from bs4 import BeautifulSoup
import re

class DennerProductService:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0'
        }

    def fetch_product_details(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            title = self.extract_title(soup)
            price_info = self.extract_price_info(soup)
            weight = self.extract_weight(soup)

            product_info = {
                "Name": title,
                "Price": price_info['price'],
                "Weight": weight,
                "Nutrients": {},
                "Ingredients": None,
                "Sale Percentage": price_info['sale_percentage'],
                "Category": None,
                "URL": url
            }

            return product_info
        else:
            print(f"Failed to fetch product details. Status code: {response.status_code}")
            return None

    def extract_title(self, soup):
        title_element = soup.select_one('.titel h1')
        return title_element.text.strip() if title_element else None

    def extract_price_info(self, soup):
        price_element = soup.select_one('.aktuell.js-remove-expired')
        if price_element:
            price = price_element.contents[0].strip()
            sale_percentage = None

            sale_element = soup.select_one('.sparen.js-remove-expired')
            if sale_element:
                sale_percentage = sale_element.text.strip()

            return {'price': price, 'sale_percentage': sale_percentage}

        return {'price': None, 'sale_percentage': None}

    def extract_weight(self, soup):
        weight_element = soup.select_one('.beschreibung.mb-3.text-dark')
        if weight_element:
            text = weight_element.text.strip()
            # Suche nach dem letzten Komma und extrahiere den Teil danach
            parts = text.split(',')
            if parts:
                last_part = parts[-1].strip()
                # Suche nach einer Volumen- oder Gewichtsangabe
                match = re.search(r'(\d+(?:\.\d+)?)\s*(cl|ml|l|g|kg)', last_part)
                if match:
                    return match.group()
        return None
