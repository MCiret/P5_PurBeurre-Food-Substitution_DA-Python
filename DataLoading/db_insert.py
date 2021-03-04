from mysql import connector as db


def db_insert_all_products(json_products: list, db_connector) -> dict:
    """/!/ json_products has to be a list of valid products dicts (i.e
    returned from off_json_data.make_list_of_all_valid_products() function).
    1 product <=> 1 food
    """
    db_curs = db_connector.cursor()
    prod_inserted = 0
    cat_inserted = 0
    store_inserted = 0
    for prod_dict in json_products:
        prod_inserted += food_db_insert(db_curs, db_connector, prod_dict)
        cat_inserted += categories_db_insert(db_curs, db_connector, prod_dict["_id"],
                             prod_dict["categories_tags"])
        # Reminder : "stores_tags" field is optional
        if "stores_tags" in prod_dict.keys():
            store_inserted += stores_db_insert(db_curs, db_connector, prod_dict["_id"],
                             prod_dict["stores_tags"])
        else:
            continue
    db_curs.close()
    db_connector.close()
    return {"to_insert": len(json_products), "prod": prod_inserted,
            "cat": cat_inserted, "store": store_inserted}


def food_db_insert(db_cursor, db_connector, food_dict: dict):
    food_insert = ("INSERT INTO food"
                   "(barcode, name, nutri_score, url_openfoodfacts,"
                   "quantity, compared_to_category)"
                   "VALUES (%s, %s, %s, %s, %s, %s)")  # f-string does not escape the '
    # Reminder : "product_quantity" field is optional
    if "product_quantity" in food_dict.keys():
        food_val = (food_dict['_id'], food_dict['product_name'],
                    food_dict['nutriscore_grade'], food_dict['url'],
                    food_dict['product_quantity'],
                    food_dict['compared_to_category'])
    else:
        food_val = (food_dict['_id'], food_dict['product_name'],
                    food_dict['nutriscore_grade'], food_dict['url'],
                    None, food_dict['compared_to_category'])
    try:
        db_cursor.execute(food_insert, food_val)
    except db.IntegrityError as err:
        print(f"\n1 {err} happens with barcode {food_dict['_id']}")
        db_connector.rollback()
        return 0
    else:
        db_connector.commit()
        return 1


def categories_db_insert(db_cursor, db_connector, food_barcode: int, food_categories_list: list):
    category_insert = "INSERT INTO category (name) VALUES (%s)"
    food_cat_insert = ("INSERT INTO food_category"
                       "(food_barcode, category_id)"
                       "VALUES (%s, %s)")
    cat_insertion = 0
    for cat in food_categories_list:
        try:
            db_cursor.execute(category_insert, (cat,))
        except db.IntegrityError:
            db_connector.rollback()
        else:
            db_connector.commit()
            cat_insertion += 1
        finally:
            db_cursor.execute(f"SELECT id FROM category WHERE name = %s", (cat,))
            cat_id = db_cursor.fetchone()[0]
            try:
                db_cursor.execute(food_cat_insert, (food_barcode, cat_id))
            except db.IntegrityError:
                db_connector.rollback()
            else:
                db_connector.commit()
    return cat_insertion


def stores_db_insert(db_cursor, db_connector, food_barcode: int, food_stores_list: list):
    store_insert = "INSERT INTO store (name) VALUES (%s)"
    food_store_insert = ("INSERT INTO food_store"
                         "(food_barcode, store_id)"
                         "VALUES (%s, %s)")
    store_insertion = 0
    for store in food_stores_list:
        try:
            db_cursor.execute(store_insert, (store,))
        except db.IntegrityError:
            db_connector.rollback()
        else:
            db_connector.commit()
            store_insertion += 1
        finally:
            db_cursor.execute(f"SELECT id FROM store WHERE name = %s", (store,))
            store_id = db_cursor.fetchone()[0]
            try:
                db_cursor.execute(food_store_insert, (food_barcode, store_id))
            except db.IntegrityError:
                db_connector.rollback()
            else:
                db_connector.commit()
    return store_insertion


# my tests
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
