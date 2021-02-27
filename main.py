import off_json_data as dt
import pur_beurre_db as db
import config as cfg


def main():
    print("off_json_data.py ...")
    curr_responses_list = dt.get_json_data_from_off_api()
    curr_products_list = dt.make_list_of_all_valid_products(curr_responses_list)
    dt.select_and_translate_products_categories(curr_products_list)
    print("\npur_beurre_db.py ...")
    conn = db.db_connection(cfg.DB_PARAM)
    curs = db.get_db_cursor(conn)
    # db.db_insert_my_tests(conn, curs)
    db.db_insert_products(curr_products_list, conn, curs)


if __name__ == '__main__':
    main()
