from foodsubstitution.views.data_init_view import DataInitView
import dataoff.off_api_data as dt
import dataoff.myUtils_tmp as mu
from foodsubstitution.models.food_model import Food

class DataInitControl:


    view = DataInitView()
    args = view.get_run_args()
    
    @classmethod
    def run_data_initialization(cls):
        """OFF search API data are : get, reorganized and inserted into the
        local database (for the moment, db is created by executing
        pur_beurre_db_creation.sql out of this python program)"""

        if cls.args.load_data:
            if cls.args.verbose:
                cls.view.data_initialization_step(1)
            if cls.args.page != cls.view.page_arg_def_val:
                curr_responses_list = dt.get_off_api_data(cls.args.page)
            else:
                curr_responses_list = dt.get_off_api_data(cls.view.page_arg_def_val)
            if cls.args.verbose:
                cls.view.step_done()
            
            if not dt.check_off_data_gotten(curr_responses_list):
                cls.view.no_data_initialization_error()
                exit()

            ########################################################
            mu.sort_write_json_resp_by_category(curr_responses_list)  # my json writing to check data... => to be deleted !
            ########################################################
            
            if cls.args.verbose:
                cls.view.data_initialization_step(2)
            curr_valid_products_list = dt.build_list_of_all_valid_products(
                curr_responses_list)
            if cls.args.verbose:
                cls.view.step_done()
            
            if cls.args.verbose:
                cls.view.data_initialization_step(3)
            dt.select_and_translate_products_categories(curr_valid_products_list)
            if cls.args.verbose:
                cls.view.step_done()
            
            ########################################################
            mu.write_valid_products(curr_valid_products_list)  # my json writing to check data... => to be deleted !
            ########################################################

            if cls.args.verbose:
                cls.view.data_initialization_step(4)
            insert_results_counts_dict = Food.objects.insert_all_foods(curr_valid_products_list)
            if cls.args.verbose:
                cls.view.step_done()
                cls.view.data_loading_results(insert_results_counts_dict)

        else:
            cls.view.no_data_initialization_asked_by_user()
