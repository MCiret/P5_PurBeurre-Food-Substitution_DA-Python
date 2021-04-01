import foodsubstitution.models as m

class StoreManager:
    """
    Access to database to select/insert data from/in Store table.
    Select queries creates Store objects.
    """

    def __init__(self, db_connection, db_connector):
        self.db_connection = db_connection
        self.db_connector = db_connector
    
    def get_all_by_food(self, food_id: int) -> 'list[Store] (empty if nothing found)':
        """
        To get and instance Store objects for one Food.
        Joined Food not gotten (i.e attribute foods_store is None).
        """
        assert(type(food_id) is int)
        
        curs = self.db_connection.cursor()
        store_list = []
        curs.execute("SELECT * "
                     "FROM store as s "
                     "JOIN food_store as fs "
                     "ON (s.id = fs.store_id) "
                     "JOIN food as f "
                     "ON (f.barcode = fs.food_barcode) "
                     "WHERE f.barcode = (%s)", (food_id,))
        # a Store could have 0...* Food(s)
        for store in curs.fetchall():  # fetchall() returns [] if query results set is empty ; fetchone() returns None in same case
            store_obj = m.Store(store[1])
            store_obj.id = store[0]
            store_list.append(store_obj)
                
        curs.close()
        return store_list

    def insert_stores_food(self, food_barcode: int, food_stores_list: list) -> 'int (number of stores inserted)':
        assert(type(food_barcode) is int and type(food_stores_list) is list)

        curs = self.db_connection.cursor()
        store_insert = "INSERT INTO store (name) VALUES (%s)"
        food_store_insert = ("INSERT INTO food_store"
                            "(food_barcode, store_id)"
                            "VALUES (%s, %s)")
        store_insertion = 0
        for store in food_stores_list:
            try:
                curs.execute(store_insert, (store,))
            except self.db_connector.IntegrityError:
                self.db_connection.rollback()
            else:
                self.db_connection.commit()
                store_insertion += 1
            finally:
                curs.execute(f"SELECT id FROM store WHERE name = %s", (store,))
                store_id = curs.fetchone()[0]
                try:
                    curs.execute(food_store_insert, (food_barcode, store_id))
                except self.db_connector.IntegrityError:
                    self.db_connection.rollback()
                else:
                    self.db_connection.commit()

        curs.close()
        return store_insertion
