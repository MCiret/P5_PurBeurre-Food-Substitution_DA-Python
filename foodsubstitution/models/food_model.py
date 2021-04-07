from database_managers.food_manager import FoodManager
from database_managers.db_connection import db_connection_activate, db_connector
from dataclasses import dataclass, field


@dataclass
class Food:
    """Food objects initialized in database SELECT queries"""

    objects = FoodManager(db_connection_activate, db_connector)

    id: int = field(init=False, default=None)  # equivalent for barcode field

    # attribute not involved in tables relations
    name: str = field(default=None)
    nutriscore: str = field(default=None)
    url_openfoodfacts: str = field(default=None)
    quantity: str = field(default=None)
    compared_to_category: str = field(default=None)
    # representing tables relations
    categories_food: 'list[Category]' = field(default=None)
    stores_food: 'list[Store]' = field(default=None)
