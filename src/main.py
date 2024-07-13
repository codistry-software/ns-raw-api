from config.flask_config import create_app
from webshops.controller import WebshopController

def main():
    app = create_app()
    webshop_controller = WebshopController()
    webshop_controller.process_webshops()

if __name__ == "__main__":
    main()
