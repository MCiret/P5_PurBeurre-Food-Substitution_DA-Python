"""Database layer access and handling of models instances
(inserting, selecting, etc...)
Look OC Webinaire (T. Chappuis) "BD - AOO - Orga du code"
"""

import foodsubstitution.models as m
from database import db_connection as dbc

class FoodManager:

    def __init__(self, db):
        self.db = db

    def get_all_by_category(self, category_id: int) -> 'list[Food] (empty if nothing found)':
        """To get and instance Food objects in one Category.
        Joined Category and Store not gotten (i.e attributes categories_food and
        stores_food are None)."""
        curs = self.db.cursor()
        food_list = []
        curs.execute("SELECT * "
                     "FROM food as f "
                     "JOIN food_category as fc "
                     "ON (f.barcode = fc.food_barcode) "
                     "JOIN category as c "
                     "ON (c.id = fc.category_id) "
                     "WHERE c.id = (%s) ORDER BY f.name", (category_id,))
        # a Food have 1...* Category(ies)
        for food in curs.fetchall():  # fetchall() returns [] if query result set is empty ; fetchnone() returns None in the same case
            food_obj = m.Food(*food[1:6])
            food_obj.id = food[0]
            food_list.append(food_obj)

        curs.close()
        return food_list
    
    def get_all_by_ctc_and_nutriscore_better_than(self, substituted_food: 'Food') -> 'list[SubstituteFood] (empty if nothing found)':
        """ Get relevant substitutes list (i.e Foods with same compared_to_category
        but better nutriscore than :param substituted_food). For each substitute Food, joined
        Category and Store are gotten.""" 
        curs = self.db.cursor()
        subfood_list = []
        curs.execute("SELECT * FROM food as f "
                     "WHERE f.compared_to_category = (%s)"
                     "AND f.nutriscore < (%s)",
                    (substituted_food.compared_to_category , substituted_food.nutriscore))
        # a Food could have 0...* SubstituteFood
        for subfood in curs.fetchall():
            subfood_obj = m.SubstitutionFood(*subfood[1:], substituted_food=substituted_food)
            subfood_obj.id = subfood[0]
            subfood_obj.categories_food = m.Category.objects.get_all_by_food(subfood_obj.id)
            subfood_obj.stores_food = m.Store.objects.get_all_by_food(subfood_obj.id)

            subfood_list.append(subfood_obj)

        curs.close()
        return subfood_list

    def get_all_by_compared_to_category(self, substituted_food_id: int, substituted_food_ctc: str) -> 'list[Food] (empty if nothing found)':
        """ Get relevant comparable foods list (i.e with same compared_to_category).""" 
        curs = self.db.cursor()
        simfood_list = []
        curs.execute("SELECT * "
                     "FROM food as f "
                     "WHERE f.compared_to_category = (%s) "
                     "AND f.barcode != (%s)",
                     (substituted_food_ctc, substituted_food_id))
        for simfood in curs.fetchall():
            simfood_obj = m.Food(*simfood[1:])
            simfood_obj.id = simfood[0]
            simfood_obj.categories_food = m.Category.objects.get_all_by_food(simfood_obj.id) 
            simfood_obj.stores_food = m.Store.objects.get_all_by_food(simfood_obj.id)

            simfood_list.append(simfood_obj)
        curs.close()
        return simfood_list
  
    def save_bookmark(self, substitution_food_id: int, substituted_food_id: int) -> 'bool (insertion success/failure)':
        curs = self.db.cursor()
        try:
            curs.execute("INSERT INTO bookmark "
                         "(food_barcode, substitute_barcode) "
                         "VALUES (%s, %s)",
                        (substituted_food_id, substitution_food_id))
        except dbc.db_connector.IntegrityError:
            self.db.rollback()
            curs.close()
            return False
        else:
            self.db.commit()
            curs.close()
            return True
    
    def get_all_bookmarks_name_id_nutriscore(self) -> 'list[SubstitutionFood]':
        curs = self.db.cursor()
        bk_list = []
        curs.execute("SELECT fs.barcode, fs.name, fs.quantity, fs.nutriscore, fd.barcode, fd.name, fd.quantity, fd.nutriscore "
                     "FROM food as fs "
                     "JOIN bookmark as bk ON (fs.barcode = bk.substitute_barcode) "
                     "JOIN food as fd ON (fd.barcode = bk.food_barcode)")
        for bookmark in curs.fetchall():
            bk_obj = m.SubstitutionFood(name=bookmark[1], quantity=bookmark[2], nutriscore=bookmark[3], 
                                        substituted_food=m.Food(name=bookmark[5], quantity=bookmark[6], nutriscore=bookmark[7]))
            bk_obj.id = bookmark[0]
            bk_obj.substituted_food.id = bookmark[4]
            bk_list.append(bk_obj)

        curs.close()
        return bk_list
    
    def get_one_bookmark_all_infos(self, substitution_food_id: int, substituted_food_id: int) -> 'SubstitutionFood':
        curs = self.db.cursor()
        curs.execute("SELECT * FROM food as fs "
                     "JOIN bookmark as bk ON (fs.barcode = bk.substitute_barcode) "
                     "JOIN food as fd ON (fd.barcode = bk.food_barcode) "
                     "WHERE fs.barcode = (%s) AND fd.barcode = (%s)",
                     (substitution_food_id, substituted_food_id))
        subfood = curs.fetchone()
        subfood_obj = m.SubstitutionFood(*subfood[1:6])
        subfood_obj.id = subfood[0]
        subfood_obj.categories_food = m.Category.objects.get_all_by_food(subfood_obj.id)
        subfood_obj.stores_food = m.Store.objects.get_all_by_food(subfood_obj.id)
        subfood_obj.substituted_food = m.Food(*subfood[9:])
        subfood_obj.substituted_food.id = subfood[8]

        curs.close()
        return subfood_obj

    def create(self, id:"barcode", name, nutriscore, url_openfoodfacts,
               quantity, compared_to_category, categories, stores):
        pass

    # Etc... => all needed and specific methods


class CategoryManager:

    def __init__(self, db):
        self.db = db

    def get_all(self) -> 'list[Category] (empty if nothing found)':
        """To get and instance Category objects with all categories from DB.
        Joined Food not gotten (i.e attribute foods_category is None).
        """
        curs = self.db.cursor()
        cat_list = []
        curs.execute("SELECT * FROM category")
        for cat_res in curs.fetchall():  # fetchall() returns [] if query result set is empty ; fetchnone() returns None in the same case
            cat_obj = m.Category(cat_res[1])
            cat_obj.id = cat_res[0]
            cat_list.append(cat_obj)

        curs.close()
        return cat_list

    def get_all_by_food(self, food_id: int) -> 'list[Category] (empty if nothing found)':
        """To get and instance Category objects for one Food.
        Joined Food not gotten (i.e attribute foods_category is None)."""
        curs = self.db.cursor()
        cat_list = []
        curs.execute("SELECT * "
                     "FROM category as c "
                     "JOIN food_category as fc "
                     "ON (c.id = fc.category_id) "
                     "JOIN food as f "
                     "ON (f.barcode = fc.food_barcode)"
                     "WHERE f.barcode = (%s)", (food_id,))
        # a Category could have 0...* Food(s)
        for cat in curs.fetchall():
            cat_obj = m.Category(cat[1])
            cat_obj.id = cat[0]
            cat_list.append(cat_obj)

        curs.close()
        return cat_list
 

class StoreManager:
    def __init__(self, db):
        self.db = db
    
    def get_all_by_food(self, food_id: int) -> 'list[Store] (empty if nothing found)':
        """To get and instance Store objects for one Food.
        Joined Food not gotten (i.e attribute foods_store is None)."""
        curs = self.db.cursor()
        store_list = []
        curs.execute("SELECT * "
                     "FROM store as s "
                     "JOIN food_store as fs "
                     "ON (s.id = fs.store_id) "
                     "JOIN food as f "
                     "ON (f.barcode = fs.food_barcode) "
                     "WHERE f.barcode = (%s)", (food_id,))
        # a Store could have 0...* Food(s)
        for store in curs.fetchall():  # NB: fetchall() returns [] if query results set is empty ; fetchone() returns None in same case
            store_obj = m.Store(store[1])
            store_obj.id = store[0]
            store_list.append(store_obj)
                
        curs.close()
        return store_list
