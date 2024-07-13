import psycopg2
from psycopg2 import sql
from psycopg2.extras import Json
from webshops.dto.product_dto import ProductDTO
from config.db_config import DB_CONFIG

class MigrosRepository:
    def __init__(self):
        self.connection = psycopg2.connect(**DB_CONFIG)

    def insert_product(self, product: ProductDTO):
        with self.connection.cursor() as cursor:
            query = sql.SQL("""
                INSERT INTO products (name, description, price, availability, category, sale, ingredients, nutritional_info)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """)
            cursor.execute(query, (
                product.name,
                product.description,
                product.price,
                product.availability,
                product.category,
                product.sale,
                product.ingredients,
                Json(product.nutritional_info)
            ))
            self.connection.commit()

    def close(self):
        self.connection.close()
