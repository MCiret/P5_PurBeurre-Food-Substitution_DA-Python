"""Data handling (no database direct access)
Look OC Webinaire (T. Chappuis) "BD - AOO - Orga du code"
"""

from Database.db_managers import FoodManager
from Database.db_managers import CategoryManager
from Database.db_managers import StoreManager
from Database.db_connection import db_connection_activate
from dataclasses import dataclass, field  # https://realpython.com/python-data-classes/#more-flexible-data-classes
from typing import List


@dataclass
class Food:
    """Initialize a food object but isn't in charge of database inserting"""

    objects = FoodManager(db_connection_activate)  # Django style

    
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
    categories_food: 'List[Category]' = field(default=None)
    stores_food: 'List[Store]' = field(default=None)

@dataclass
class SubstitutionFood(Food):
    """A Food object with same compared_to_category but better nutriscore than
    the substituted Food object (which has been selected by user)"""

    substituted_food: Food = field(default=None)

@dataclass
class Category:

    objects = CategoryManager(db_connection_activate)  # Django style

    # id (PK in db) is not in init parameters because we don't want
    # to initialise it "by hand" => it has to be handle by managers..
    id: int = field(init=False, default=None)
    name: str = field(default=None)  # attribute not involved in tables relations
    foods_category: List[Food] = field(default=None)  # attribute involved in/representing tables relations


@dataclass
class Store:

    objects = StoreManager(db_connection_activate)  # Django style

    # id (PK in db) is not in init parameters because we don't want
    # to initialise it "by hand" => it has to be handle by managers..
    id: int = field(init=False, default=None)
    name: str = field(default=None)  # attribute not involved in tables relations
    foods_store: List[Food] = field(default=None)  # attribute involved in/representing tables relations

