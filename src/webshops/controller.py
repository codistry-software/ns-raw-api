import json
from webshops.migros.controller import MigrosController
from webshops.coop.controller import CoopController
from webshops.denner.controller import DennerController

class WebshopController:
    def __init__(self):
        self.webshops = {
            'migros': MigrosController(),
            'coop': CoopController(),
            'denner': DennerController()
        }
        self.search_terms = self.load_search_terms()

    def load_search_terms(self):
        with open('search_queries/queries.json', 'r') as file:
            data = json.load(file)
        return data['queries']

    def process_webshops(self):
        for name, controller in self.webshops.items():
            print(f"\n-----\nProcessing webshop: {name}\n-----")
            if name == 'coop':
                results = controller.process_all_pages()
                if results:
                    for product_id in results:
                        print("\nFound Product ID:", product_id)
                else:
                    print("No products found.")
            elif name == 'denner':
                print("\nProcessing all Denner products\n-----")
                results = controller.process_query('*')
                if not results:
                    print("No products found.")
                else:
                    for product in results:
                        print("\nProduct Details:\n", json.dumps(product, indent=4))
            else:
                for term in self.search_terms:
                    print(f"\nSearching for: {term}\n-----")
                    results = controller.process_query(term)
                    if not results:
                        print("No new products found for the search term.")
                    else:
                        for product in results:
                            print("\nProduct Details:\n", json.dumps(product, indent=4))
