from webshops.migros.controller import MigrosController
from src.logger.logger import logger

class WebshopController:
    def __init__(self):
        self.webshops = {
            'migros': MigrosController,
            # 'coop': CoopController,  # Add CoopController when available
        }

    def process_webshops(self):
        for name, Controller in self.webshops.items():
            logger.info(f"Processing webshop: {name}")
            controller = Controller()
            product_ids = controller.fetch_product_ids("fleisch")
            if not product_ids:
                logger.warning(f"No product IDs found for {name}")
                continue

            migros_ids = controller.fetch_migros_ids(product_ids)
            for migros_id in migros_ids:
                product_details = controller.fetch_product_details(migros_id)
                if product_details:
                    logger.info(product_details)
