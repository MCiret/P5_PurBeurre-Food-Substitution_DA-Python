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

    # attribute not involved in tables relations
    name: str
    nutri_score: str
    url_openfoodfacts : str
    quantity: str
    compared_to_category: str
    # attribute involved in/representing tables relations
    categories: 'List[Category]'
    stores: 'List[Store]'

    # id (PK in db) is not in init parameters because we don't want
    # to initialise it "by hand" => it has to be handle by managers..
    id: int = field(init=False, default=None)  # here it is the barcode field ;


@dataclass
class Category:

    objects = CategoryManager(dbc.db_active_connection)  # Django style

    name: str  # attribute not involved in tables relations
    food_category: List[Food]  # attribute involved in/representing tables relations

    # id (PK in db) is not in init parameters because we don't want
    # to initialise it "by hand" => it has to be handle by managers..
    id: int = field(init=False, default=None)


@dataclass
class Store:

    objects = StoreManager(dbc.db_active_connection)  # Django style

    name: str  # attribute not involved in tables relations
    food_store: List[Food]  # attribute involved in/representing tables relations

    # id (PK in db) is not in init parameters because we don't want
    # to initialise it "by hand" => it has to be handle by managers..
    id: int = field(init=False, default=None)

