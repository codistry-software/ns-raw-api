import json
# from webshops.migros.controller import MigrosController
from webshops.coop.controller import CoopController  # Assuming you will create this

class WebshopController:
    def __init__(self):
        self.webshops = {
            # 'migros': MigrosController(),  # Commented out for testing
            'coop': CoopController()  # Add Coop controller
        }
        self.search_terms = self.load_search_terms()

    def load_search_terms(self):
        with open('search_queries/queries.json', 'r') as file:
            data = json.load(file)
        return data['queries']

    def process_webshops(self):
        for name, controller in self.webshops.items():
            print(f"\n-----\nProcessing webshop: {name}\n-----")
            for term in self.search_terms:
                print(f"\nSearching for: {term}\n-----")
                results = controller.process_query(term)
                if not results:
                    print("No new products found for the search term.")
                else:
                    for product in results:
                        print("\nProduct Details:\n", json.dumps(product, indent=4))
