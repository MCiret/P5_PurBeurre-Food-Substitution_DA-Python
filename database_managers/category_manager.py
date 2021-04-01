import foodsubstitution.models as m

class CategoryManager:
    """
    Access to database to select/insert data from/in Category table.
    Select queries creates Category objects.
    """

    def __init__(self, db_connection, db_connector):
        self.db_connection = db_connection
        self.db_connector = db_connector

    def get_all(self) -> 'list[Category] (empty if nothing found)':
        """
        To get and instance Category objects with all categories from DB.
        Joined Food not gotten (i.e attribute foods_category is None).
        """
        curs = self.db_connection.cursor()
        cat_list = []
        curs.execute("SELECT * FROM category")
        for cat_res in curs.fetchall():  # fetchall() returns [] if query result set is empty ; fetchnone() returns None in the same case
            cat_obj = m.Category(cat_res[1])
            cat_obj.id = cat_res[0]
            cat_list.append(cat_obj)

        curs.close()
        return cat_list

    def get_all_by_food(self, food_id: int) -> 'list[Category] (empty if nothing found)':
        """
        To get and instance Category objects for one Food.
        Joined Food not gotten (i.e attribute foods_category is None).
        """
        assert(type(food_id) is int)

        curs = self.db_connection.cursor()
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

    def insert_categories_food(self, food_barcode: int, food_categories_list: list) -> 'int (number of categories inserted)':
        assert(type(food_barcode) is int and type(food_categories_list) is list)
        
        curs = self.db_connection.cursor()
        category_insert = "INSERT INTO category (name) VALUES (%s)"
        food_cat_insert = ("INSERT INTO food_category"
                           "(food_barcode, category_id)"
                           "VALUES (%s, %s)")
        cat_insertion = 0
        for cat in food_categories_list:
            try:
                curs.execute(category_insert, (cat,))
            except self.db_connector.IntegrityError:
                self.db_connection.rollback()
            else:
                self.db_connection.commit()
                cat_insertion += 1
            finally:
                curs.execute(f"SELECT id FROM category WHERE name = %s", (cat,))
                cat_id = curs.fetchone()[0]
                try:
                    curs.execute(food_cat_insert, (food_barcode, cat_id))
                except self.db_connector.IntegrityError:
                    self.db_connection.rollback()
                else:
                    self.db_connection.commit()
        curs.close()
        return cat_insertion
