"""Data handling (no database direct access)
Look OC Webinaire (T. Chappuis) "BD - AOO - Orga du code"
"""

from db_managers import FoodManager
from db_managers import CategoryManager
from db_managers import StoreManager
import DataLoading.database_connection as db


class Food:

    objects = FoodManager(db)  # Django style

    def __init__(self, name, nutri_score, url_openfoodfacts,
                 quantity, compared_to_category, categories, stores):
        # id (PK in db) is not in init parameters because we don't want
        # to initialise it "by hand"
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

    objects = CategoryManager(db)  # Django style

    def __init__(self, name, foods_category):
        # id (PK in db) is not in init parameters because we don't want
        # to initialise it "by hand"
        self.id = None
        # attribute not involved in tables relations
        self.name = name
        # attribute involved in/representing tables relations
        self.foods_category = foods_category


class Store:

    objects = StoreManager(db)  # Django style

    def __init__(self, name, foods_store):
        # id (PK in db) is not in init parameters because we don't want
        # to initialise it "by hand"
        self.id = None
        # attribute not involved in tables relations
        self.name = name
        # attribute involved in/representing tables relations
        self.foods_store = foods_store
