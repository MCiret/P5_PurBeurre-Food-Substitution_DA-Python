from foodsubstitution.views.data_init_view import DataInitView
import dataoff.off_api_data as dt
from foodsubstitution.models.food_model import Food

class DataInitControl:
    """ Manages data from OFF search API : get, reorganization and insertion 
    into the local database (reminder : this database has to be created by
    executing pur_beurre_db_creation.sql apart from this python program).
    Also manages the command-line argument(s) such as calls his view to
    display proceedings steps, potential error/problem and some results about
    data gotten and inserted.
    """

    view = DataInitView()
    args = view.get_run_args()
    
    @classmethod
    def run_data_initialization(cls):
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

            if cls.args.verbose:
                cls.view.data_initialization_step(4)
            insert_results_counts_dict = Food.objects.insert_all_foods(curr_valid_products_list)
            if cls.args.verbose:
                cls.view.step_done()
                cls.view.data_loading_results(insert_results_counts_dict)

        else:
            cls.view.no_data_initialization_asked_by_user()
