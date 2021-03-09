"""Database layer access and handling of models instances
(inserting, selecting, etc...)
Look OC Webinaire (T. Chappuis) "BD - AOO - Orga du code"
"""

import FoodSubstitution.models as m

class FoodManager:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        # rows = db.curs.execute("SELECT * FROM food")
        # actually, for each food we would like to retrieve associated
        # categories and potential stores
        # to build all the structure of a Movie() object
        curs = self.db.cursor()
        curs.execute("SELECT barcode, name, nutri_score, url_openfoodfacts, "
                     "quantity, compared_to_category "
                     "FROM food")
        food_list = []
        for food_row in curs.fetchall():
            fd_id = food_row[0]
            fd_categories = []
            fd_stores = []
            cat_curs = self.db.cursor()
            store_curs = self.db.cursor()
            cat_curs.execute("SELECT c.name "
                            "FROM category as c "
                            "JOIN food_category as fc "
                            "ON (c.id = fc.category_id) "
                            "JOIN food as f "
                            "ON (f.barcode = fc.food_barcode) "
                            "WHERE f.barcode = (%s)", (fd_id,))
            for cat_row in cat_curs.fetchall():
                fd_categories.append(cat_row)
                print(f"Food {fd_id} --> in category {cat_row} ")
            store_curs.execute("SELECT s.name "
                            "FROM store as s "
                            "JOIN food_store as fs "
                            "ON (s.id = fs.store_id) "
                            "JOIN food as f "
                            "ON (f.barcode = fs.food_barcode) "
                            "WHERE f.barcode = (%s)", (fd_id,))
            for store_row in store_curs.fetchall():
               fd_stores.append(store_row)
               print(f"Food {fd_id} --> in store {store_row}")
            
            fd = m.Food(*food_row[1:], fd_categories, fd_stores)
            fd.id = fd_id
            food_list.append(fd)
            print("1 food OK : ", fd)

        print(len(food_list))

    def get_all_by_category(self, category):  # for example
        pass

    def get_all_with_nutriscore_better_than(self, nutriscore):  # for example
        pass

    def save(self, food):
        pass

    def create(self, id:"barcode", name, nutri_score, url_openfoodfacts,
               quantity, compared_to_category, categories, stores):
        pass

    # Etc... => all needed and specifics methods


class CategoryManager:
    def __init__(self, db):
        self.db = db


class StoreManager:
    def __init__(self, db):
        self.db = db
    pass
