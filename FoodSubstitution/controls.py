import views as v
import Data.get_off_api_data as dt
from Database import db_insertion as dbi
from Database import db_connection as dbc
import Data.myUtils_tmp as mu


def load_data():
    args = v.get_args()
    if args.load_data:
        v.display_data_loading_step(1)
        curr_responses_list = dt.get_off_api_data(args.page)
        v.display_done_msg()

        mu.sort_write_json_resp_by_category(curr_responses_list)

        v.display_data_loading_step(2)
        curr_valid_products_list = dt.build_list_of_all_valid_products(
            curr_responses_list)
        v.display_done_msg()

        v.display_data_loading_step(3)
        dt.select_and_translate_products_categories(curr_valid_products_list)
        v.display_done_msg()

        mu.write_valid_products(curr_valid_products_list)

        v.display_data_loading_step(4)
        insert_results_counts_dict = dbi.db_insert_all_products(curr_valid_products_list, dbc)
        v.display_done_msg()

        v.display_db_insertions_counts(insert_results_counts_dict)

    else:
        v.display_no_data_loading()

