"""Data handling (no database direct access)
Look OC Webinaire (T. Chappuis) "BD - AOO - Orga du code"
"""

from Database.db_managers import FoodManager
from Database.db_managers import CategoryManager
from Database.db_managers import StoreManager
import Database.db_connection as dbc
from dataclasses import dataclass, field  # https://realpython.com/python-data-classes/#more-flexible-data-classes
from typing import List


@dataclass
class Food:
    """Initialize a food object but isn't in charge of database inserting"""

    objects = FoodManager(dbc.db_active_connection)  # Django style

    
    # id (PK in db) is not in init parameters because we don't want
    # to initialise it "by hand" => it has to be handle by managers..
    id: int = field(init=False, default=None)  # here it is the barcode field ;
    
    # attribute not involved in tables relations
    name: str = field(default=None)
    nutri_score: str = field(default=None) 
    url_openfoodfacts : str = field(default=None)
    quantity: str = field(default=None)
    compared_to_category: str = field(default=None)
    # attribute involved in/representing tables relations
    categories: 'List[Category]' = field(default=None)
    stores: 'List[Store]' = field(default=None)


@dataclass
class Category:

    objects = CategoryManager(dbc.db_active_connection)  # Django style

    # id (PK in db) is not in init parameters because we don't want
    # to initialise it "by hand" => it has to be handle by managers..
    id: int = field(init=False, default=None)
    name: str = field(default=None)  # attribute not involved in tables relations
    food_category: List[Food] = field(default=None)  # attribute involved in/representing tables relations


@dataclass
class Store:

    objects = StoreManager(dbc.db_active_connection)  # Django style

    # id (PK in db) is not in init parameters because we don't want
    # to initialise it "by hand" => it has to be handle by managers..
    id: int = field(init=False, default=None)
    name: str = field(default=None)  # attribute not involved in tables relations
    food_store: List[Food] = field(default=None)  # attribute involved in/representing tables relations

