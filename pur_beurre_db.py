from mysql import connector as db


def db_insert_all_products(json_products: list, db_connection_params: dict):
    """/!/ json_products has to be a list of valid products dicts (i.e
    returned from off_json_data.make_list_of_all_valid_products() function).
    1 product <=> 1 food
    """
    db_conn = db.connect(**db_connection_params)
    db_curs = db_conn.cursor()
    nb_prod_tot = len(json_products)
    nb_prod = 0
    for prod_dict in json_products:
        nb_prod += 1
        food_db_insert(db_curs, db_conn, prod_dict)
        categories_db_insert(db_curs, db_conn, prod_dict["_id"],
                             prod_dict["categories_tags"])
        # a product could not have a "stores_tags" value
        try:
            stores_db_insert(db_curs, db_conn, prod_dict["_id"],
                             prod_dict["stores_tags"])
        except KeyError:
            continue
        if nb_prod % 50 == 0 or nb_prod == nb_prod_tot:
            print(f"=========== food n° {nb_prod}/{nb_prod_tot} ===========\n")
    db_curs.close()
    db_conn.close()


def food_db_insert(db_cursor, db_connector, food_dict):
    food_insert = ("INSERT INTO food"
                   "(barcode, name, nutri_score, url_openfoodfacts,"
                   "quantity, compared_to_category)"
                   "VALUES (%s, %s, %s, %s, %s, %s)")  # f-string does not escape the '
    try:
        food_val = (food_dict['_id'], food_dict['product_name'],
                    food_dict['nutriscore_grade'], food_dict['url'],
                    food_dict['product_quantity'], food_dict['compared_to_category'])
        db_cursor.execute(food_insert, food_val)
    except db.IntegrityError:
        db_connector.rollback()
    except KeyError:
        food_val = (food_dict['_id'], food_dict['product_name'],
                    food_dict['nutriscore_grade'], food_dict['url'],
                    None, food_dict['compared_to_category'])
        db_cursor.execute(food_insert, food_val)
        db_connector.commit()
    else:
        db_connector.commit()


def categories_db_insert(db_cursor, db_connector, food_barcode, food_categories_list):
    category_insert = "INSERT INTO category (name) VALUES (%s)"
    food_cat_insert = ("INSERT INTO food_category"
                       "(food_barcode, category_id)"
                       "VALUES (%s, %s)")
    for cat in food_categories_list:
        try:
            db_cursor.execute(category_insert, (cat,))
        except db.IntegrityError:
            db_connector.rollback()
        else:
            db_connector.commit()
        finally:
            db_cursor.execute(f"SELECT id FROM category WHERE name = %s", (cat,))
            cat_id = db_cursor.fetchone()[0]
            db_cursor.execute(food_cat_insert, (food_barcode, cat_id))
            db_connector.commit()


def stores_db_insert(db_cursor, db_connector, food_barcode, food_stores_list):
    store_insert = "INSERT INTO store (name) VALUES (%s)"
    food_store_insert = ("INSERT INTO food_store"
                         "(food_barcode, store_id)"
                         "VALUES (%s, %s)")
    for store in food_stores_list:
        try:
            db_cursor.execute(store_insert, (store,))
        except db.IntegrityError:
            db_connector.rollback()
        else:
            db_connector.commit()
        finally:
            db_cursor.execute(f"SELECT id FROM store WHERE name = %s", (store,))
            store_id = db_cursor.fetchone()[0]
            db_cursor.execute(food_store_insert, (food_barcode, store_id))
            db_connector.commit()


def db_insert_my_tests(db_connector: 'MySQL db connector',
                    db_cursor: 'MySQL db cursor'):

    db_cursor.execute(f'INSERT INTO category'
                      f'(name)'
                      f'VALUES ("pizza")')
    print(db_cursor.lastrowid)
    db_cursor.execute(f'INSERT INTO category'
                      f'(name)'
                      f'VALUES ("pain")')
    print(db_cursor.lastrowid)
    db_connector.commit()
    db_cursor.close()
    db_connector.close()
