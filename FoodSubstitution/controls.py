import FoodSubstitution.views as v
import FoodSubstitution.models as m
import Data.get_off_api_data as dt
from Database import db_insertion as dbi
from Database import db_connection as dbc
import Data.myUtils_tmp as mu


def initialize_data():
    """OFF search API data are : get, reorganized and inserted into the
    local database (for the moment, db is created by executing
    pur_beurre_db_creation.sql out of this python program)"""
    run_view = v.RunView()
    args = run_view.get_run_args()
    if args.load_data:
        run_view.data_initialization_step(1)
        if args.page != run_view.page_arg_def_val:
            curr_responses_list = dt.get_off_api_data(args.page)
        else:
            curr_responses_list = dt.get_off_api_data(run_view.page_arg_def_val)
        run_view.step_done()

        mu.sort_write_json_resp_by_category(curr_responses_list)

        run_view.data_initialization_step(2)
        curr_valid_products_list = dt.build_list_of_all_valid_products(
            curr_responses_list)
        run_view.step_done()

        run_view.data_initialization_step(3)
        dt.select_and_translate_products_categories(curr_valid_products_list)
        run_view.step_done()

        mu.write_valid_products(curr_valid_products_list)

        run_view.data_initialization_step(4)
        insert_results_counts_dict = dbi.db_insert_all_products(curr_valid_products_list, dbc.db_connector, dbc.db_active_connection)
        run_view.step_done()

        run_view.data_loading_results(insert_results_counts_dict)
    else:
        run_view.no_data_initialization()
        # m.Food.objects.get_all()
        curr_foods_list = m.Food.objects.get_all()
        print(f"Foods instances in the list = {len(curr_foods_list)}")
        for food in curr_foods_list:
            print(food.id, food.name, food.nutri_score, food.url_openfoodfacts,
                  food.quantity, food.compared_to_category)
            print(f"--> in categories {food.categories}")
            print(f"--> in stores {food.stores}")




