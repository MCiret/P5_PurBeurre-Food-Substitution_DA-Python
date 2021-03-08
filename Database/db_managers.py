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
        curs.execute("SELECT * FROM food")
        # for row in curs.fetchall():
            # print(row)
        food_list = []
        for row in curs.fetchall():
            fd = m.Food(*row[1:])
            fd.id = row[0]
            food_list.append(fd)

        for food in food_list:
            print(type(food))

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
