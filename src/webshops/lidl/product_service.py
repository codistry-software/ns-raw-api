import requests
from bs4 import BeautifulSoup
import re
import json


class LidlProductService:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
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
        title_element = soup.select_one('.page-title-wrapper.product .page-title .base')
        return title_element.text.strip() if title_element else None

    def extract_price_info(self, soup):
        price_box = soup.select_one('.price-box.price-final_price')
        if price_box:
            sale_percentage = None
            price_element = price_box.select_one('.pricefield__price')

            sale_element = price_box.select_one('.pricefield__header')
            if sale_element:
                sale_percentage = sale_element.text.strip()

            if price_element:
                price = price_element.text.strip()
                return {'price': price, 'sale_percentage': sale_percentage}

        return {'price': None, 'sale_percentage': None}

    def extract_weight(self, soup):
        weight_element = soup.select_one('.pricefield__footer')
        if weight_element:
            weight_match = re.search(r'pro (\d+g)', weight_element.text)
            if weight_match:
                return weight_match.group(1)
        return None
