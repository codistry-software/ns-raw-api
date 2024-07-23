import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urlparse

class CoopProductService:
    def __init__(self, session):
        self.session = session
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,de-CH;q=0.7,de;q=0.6',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Chromium";v="126", "Microsoft Edge";v="126", "Not A(Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }

    def fetch_product_details(self, url):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                time.sleep(random.uniform(1, 3))
                response = self.session.get(url, headers=self.headers, timeout=30)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

                title = self.safe_get_text(soup, 'h1', {'data-testauto': 'producttitle'})
                price = self.safe_get_text(soup, 'p', {'data-testauto': 'productprice'})
                weight = self.safe_get_text(soup, 'span', {'data-testauto': 'productweight'})
                ingredients = self.safe_get_text(soup, 'div', {'data-testauto': 'productingredients'})

                nutrients_dict = {}
                nutrients = soup.select('.nutritionInformation [data-testauto="nutrition-row"]')
                for nutrient in nutrients:
                    key = self.safe_get_text(nutrient, 'span', {'class': 'list--dotted-item__label-text'})
                    value = self.safe_get_text(nutrient, 'span', {'data-nutritioninformation-list-item-value': True})
                    if key and value:
                        nutrients_dict[key] = value

                sale_percentage = self.safe_get_text(soup, 'span', {'data-product-saving-text': '',
                                                                    'class': 'productBasicInfo__price-text-saving-inner'})

                parsed_url = urlparse(url)
                path_parts = parsed_url.path.split('/')
                category = [part for part in path_parts if part and part not in ('de', 'p')]
                if category and category[-1].isdigit():
                    category = category[:-1]

                product_info = {
                    "Name": title,
                    "Price": price,
                    "Weight": weight,
                    "Nutrients": nutrients_dict,
                    "Ingredients": ingredients,
                    "Sale Percentage": sale_percentage if sale_percentage else None,
                    "Category": category
                }
                return product_info

            except requests.RequestException as e:
                print(f"Attempt {attempt + 1} failed: Error fetching product details for {url}: {e}")
                if attempt == max_retries - 1:
                    print(f"Failed to load product details for {url} after {max_retries} attempts")
                    return None

            except Exception as e:
                print(f"Unexpected error occurred while processing {url}: {e}")
                return None

    def safe_get_text(self, soup, tag, attrs):
        element = soup.find(tag, attrs)
        return element.get_text(strip=True) if element else None
