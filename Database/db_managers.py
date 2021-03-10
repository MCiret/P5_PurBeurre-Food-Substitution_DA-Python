"""Database layer access and handling of models instances
(inserting, selecting, etc...)
Look OC Webinaire (T. Chappuis) "BD - AOO - Orga du code"
"""

import FoodSubstitution.models as m

class FoodManager:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        """To get and instance all foods in DB (categories and stores joins included)
        """
        food_curs = self.db.cursor()
        food_curs.execute("SELECT barcode, name, nutri_score, url_openfoodfacts, "
                     "quantity, compared_to_category "
                     "FROM food LIMIT 60")
        food_list = []
        nb_food = 0
        for food_res in food_curs.fetchall():
            nb_food += 1
            print(nb_food)
            fd_id = food_res[0]
            fd_categories = []
            cat_curs = self.db.cursor()
            cat_curs.execute("SELECT c.name "
                            "FROM category as c "
                            "JOIN food_category as fc "
                            "ON (c.id = fc.category_id) "
                            "JOIN food as f "
                            "ON (f.barcode = fc.food_barcode) "
                            "WHERE f.barcode = (%s)", (fd_id,))
            for cat_res in cat_curs:
                fd_categories.append(cat_res[0])

            store_curs = self.db.cursor()
            store_curs.execute("SELECT s.name "
                            "FROM store as s "
                            "JOIN food_store as fs "
                            "ON (s.id = fs.store_id) "
                            "JOIN food as f "
                            "ON (f.barcode = fs.food_barcode) "
                            "WHERE f.barcode = (%s)", (fd_id,))
            store_res = store_curs.fetchall()  # NB: fetchall() returns [] if query results set is empty ; fetchone() returns None in same case
            if len(store_res) != 0:
                fd_stores = []
                for store in store_res:
                    fd_stores.append(store)
                fd = m.Food(*food_res[1:], fd_categories, fd_stores)
            else:
                fd = m.Food(*food_res[1:], fd_categories)

            fd.id = fd_id
            food_list.append(fd)
        return food_list


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
