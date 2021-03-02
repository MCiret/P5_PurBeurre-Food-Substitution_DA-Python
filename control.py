import view as v
import model as m
import Data_loading.retrieve_off_api_data as dt
import Data_loading.fill_pur_beurre_db as db
import config as cfg


def load_data() -> bool:
    args = v.get_args()
    if args.ld == "Y" or args.ld == "y":
        v.display_data_loading_step(1)
        curr_responses_list = dt.get_off_api_data()
        v.display_done_msg()
        v.display_data_loading_step(2)
        curr_products_list = dt.build_list_of_all_valid_products(
            curr_responses_list)
        v.display_done_msg()
        v.display_data_loading_step(3)
        dt.select_and_translate_products_categories(curr_products_list)
        v.display_done_msg()
        v.display_data_loading_step(4)
        db.db_insert_all_products(curr_products_list, cfg.DB_PARAM)
        v.display_done_msg()
        return True

    elif args.ld == "N" or args.ld == "n":
        v.display_data_loading_step(5)
        return True

    else:
        v.display_args_error_msg(args.ld)
        return False

