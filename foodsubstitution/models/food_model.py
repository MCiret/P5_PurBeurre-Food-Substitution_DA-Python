"""Data handling (no database direct access)
Look OC Webinaire (T. Chappuis) "BD - AOO - Orga du code"
"""

from database_managers.food_manager import FoodManager
from database_managers.db_connection import db_connection_activate, db_connector
from dataclasses import dataclass, field  # https://realpython.com/python-data-classes/#more-flexible-data-classes


@dataclass
class Food:
    """Initialize a food object but isn't in charge of database inserting"""

    objects = FoodManager(db_connection_activate, db_connector)  # Django style

    
    # id (PK in db) is not in init parameters because we don't want
    # to initialise it "by hand" => it has to be handle by managers..
    id: int = field(init=False, default=None)  # here it is the barcode field ;
    
    # attribute not involved in tables relations
    name: str = field(default=None)
    nutriscore: str = field(default=None) 
    url_openfoodfacts : str = field(default=None)
    quantity: str = field(default=None)
    compared_to_category: str = field(default=None)
    # attribute involved in/representing tables relations
    categories_food: 'list[Category]' = field(default=None)
    stores_food: 'list[Store]' = field(default=None)
