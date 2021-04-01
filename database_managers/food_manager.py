import foodsubstitution.models as m

class FoodManager:
    """
    Access to database to select/insert data from/in Food table.
    Select queries creates Food (and subclass FoodSubstitution) objects.
    """

    def __init__(self, db_connection, db_connector):
        self.db_connection = db_connection
        self.db_connector = db_connector

    def get_all_by_category(self, category_id: int) -> 'list[Food] (empty if nothing found)':
        """
        Selects and instances Food objects for one Category. Joined Category and
        Store are not gotten (i.e attributes categories_food and
        stores_food are None).
        """
        assert(type(category_id) is int)

        curs = self.db_connection.cursor()
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
        """
        Get relevant substitution foods list (i.e Foods with same compared_to_category
        but better nutriscore than :param substituted_food). For each substitution Food, joined
        Category and Store are gotten.
        """
        assert(type(substituted_food) is m.Food)

        curs = self.db_connection.cursor()
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
        """
        Get relevant comparable foods list (i.e Foods with same compared_to_category than :param substituted_food).
        Called if no substitution food has been found.
        """
        assert(type(substituted_food_id) is int and type(substituted_food_ctc) is str)

        curs = self.db_connection.cursor()
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
        assert(type(substitution_food_id) is int and type(substituted_food_id) is int)

        curs = self.db_connection.cursor()
        try:
            curs.execute("INSERT INTO bookmark "
                         "(food_barcode, substitute_barcode) "
                         "VALUES (%s, %s)",
                        (substituted_food_id, substitution_food_id))
        except self.db_connector.IntegrityError:
            self.db_connection.rollback()
            curs.close()
            return False
        else:
            self.db_connection.commit()
            curs.close()
            return True
    
    def get_all_bookmarks_name_id_nutriscore(self) -> 'list[SubstitutionFood]':
        """Get all bookmarked substitution foods."""

        curs = self.db_connection.cursor()
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
        """
        Get all informations about one bookmarked substitution food
        (called when user choose to display more info).
        """
        assert(type(substituted_food_id) is int and type(substitution_food_id) is int)

        curs = self.db_connection.cursor()
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

    def insert_all_foods(self, json_products: list) -> 'dict (results of db insertions)':
        """
        Inserts foods products gotten from OFF search API.
        :param json_products has to be a list of valid products dicts
        (see foodsubstitution/controls/data_init_control.py --> run_data_initialization()).
        """
        assert(type(json_products) is list)

        prod_inserted = 0
        cat_inserted = 0
        store_inserted = 0
        for prod_dict in json_products:
            prod_inserted += self.insert_one_food(prod_dict)
            cat_inserted += m.Category.objects.insert_categories_food(prod_dict["_id"], prod_dict["categories_tags"])
            # Reminder : "stores_tags" field is optional
            if "stores_tags" in prod_dict.keys():
                store_inserted += m.Store.objects.insert_stores_food(prod_dict["_id"], prod_dict["stores_tags"])
            else:
                continue

        return {"to_insert": len(json_products), "prod": prod_inserted,
                "cat": cat_inserted, "store": store_inserted}

    def insert_one_food(self, food_dict: dict) -> 'init (1 if inserted, 0 if already in db)':
        assert(type(food_dict) is dict)
        
        curs = self.db_connection.cursor()
        food_insert = ("INSERT INTO food"
                "(barcode, name, nutriscore, url_openfoodfacts,"
                "quantity, compared_to_category)"
                "VALUES (%s, %s, %s, %s, %s, %s)")  # using f-string directly in .execute() 1st parameter does not escape the '
        # Reminder : "product_quantity" field is optional
        if "quantity" in food_dict.keys():
            food_val = (food_dict['_id'], food_dict['product_name'],
                        food_dict['nutriscore_grade'], food_dict['url'],
                        food_dict['quantity'],
                        food_dict['compared_to_category'])
        else:
            food_val = (food_dict['_id'], food_dict['product_name'],
                        food_dict['nutriscore_grade'], food_dict['url'],
                        None, food_dict['compared_to_category'])
        try:
            curs.execute(food_insert, food_val)
        except self.db_connector.IntegrityError:
            self.db_connection.rollback()
            curs.close()
            return 0
        else:
            self.db_connection.commit()
            curs.close()
            return 1

