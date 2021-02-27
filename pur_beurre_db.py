from mysql import connector as db


def db_connection(db_connection_param: dict) -> 'MySQL db connector':
    return db.connect(**db_connection_param)


def get_db_cursor(db_connector: 'MySQL db connector') -> 'MySQL db cursor':
    return db_connector.cursor()


def db_insert_products(json_products: list, db_connector: 'MySQL db connector',
                       db_cursor: 'MySQL db cursor'):
    """/!/ json_products has to be a list of valid products dicts (i.e
    returned from off_json_data.make_list_of_all_valid_products() function).
    """
    nb_prod = 0
    for prod_dict in json_products:
        nb_prod += 1
        print(f"INSERT n° {nb_prod}/350")
        food_insert = ("INSERT INTO food"
                       "(barcode, name, nutri_score, url_openfoodfacts)"
                       "VALUES (%s, %s, %s, %s)")  # escapes ' in text
        food_val = (prod_dict['_id'], prod_dict['product_name'],
                    prod_dict['nutriscore_grade'], prod_dict['url'])
        db_cursor.execute(food_insert, food_val)

        for cat in prod_dict["categories_tags"]:
            category_insert = "INSERT INTO category (name) VALUES (%s)"
            category_val = (cat,)
            db_cursor.execute(category_insert, category_val)

            food_cat_insert = ("INSERT INTO food_category"
                               "(food_barcode, category_id)"
                               "VALUES (%s, %s)")
            food_cat_val = (prod_dict['_id'], db_cursor.lastrowid)
            db_cursor.execute(food_cat_insert, food_cat_val)
    db_connector.commit()
    db_cursor.close()
    db_connector.close()


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
