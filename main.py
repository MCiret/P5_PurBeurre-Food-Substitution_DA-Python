import off_json_data as dt
import pur_beurre_db as db
import config as cfg


def main():
    curr_responses_list = dt.get_json_data_from_off_api()
    curr_products_list = dt.make_list_of_all_valid_products(curr_responses_list)
    dt.select_and_translate_products_categories(curr_products_list)
    db.db_insert_all_products(curr_products_list, cfg.DB_PARAM)


if __name__ == '__main__':
    main()
