"""Data handling (no database direct access)
Look OC Webinaire (T. Chappuis) "BD - AOO - Orga du code"
"""

from Database.db_managers import FoodManager
from Database.db_managers import CategoryManager
from Database.db_managers import StoreManager
import Database.db_connection as dbc


class Food:
    """Initialize a food object but isn't in charge of database inserting"""

    objects = FoodManager(dbc)  # Django style

    def __init__(self, name, nutri_score, url_openfoodfacts,
                 quantity, compared_to_category, categories, stores):
        # id (PK in db) is not in init parameters because we don't want
        # to initialise it "by hand" => it has to be handle by managers..
        self.id = None  # here it is the barcode field ;
        # attribute not involved in tables relations
        self.name = name
        self.nutriScore = nutri_score
        self.urlOpenFoodFacts = url_openfoodfacts
        self.quantity = quantity
        self.comparedToCategory = compared_to_category
        # attribute involved in/representing tables relations
        self.categories = categories  # list
        self.stores = stores  # list


class Category:

    objects = CategoryManager(dbc)  # Django style

    def __init__(self, name, foods_category):
        # id (PK in db) is not in init parameters because we don't want
        # to initialise it "by hand" => it has to be handle by managers..
        self.id = None
        # attribute not involved in tables relations
        self.name = name
        # attribute involved in/representing tables relations
        self.foods_category = foods_category  # list


class Store:

    objects = StoreManager(dbc)  # Django style

    def __init__(self, name, foods_store):
        # id (PK in db) is not in init parameters because we don't want
        # to initialise it "by hand" => it has to be handle by managers..
        self.id = None
        # attribute not involved in tables relations
        self.name = name
        # attribute involved in/representing tables relations
        self.foods_store = foods_store  # list
