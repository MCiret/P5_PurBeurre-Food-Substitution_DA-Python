import config as cfg
import foodsubstitution.views as vw
from .models import Food, Category, Store
from dataoff import off_api_data as dt
from database import db_insertion as dbi
from database import db_connection as dbc
from dataoff import myUtils_tmp as mu


class Controller:
    
    def __init__(self):
        self.init_view = vw.DataInitView()
        self.args = self.init_view.get_run_args()
        self.main_view = vw.MainMenuView()
        self.cat_view:'CatView' = None
        self.food_view:'FoodView' = None
        self.selected_category:'Category' = None
        self.sub_view:'SubstituteView' = None
        self.bookmarking_view = None
        self.bookmark_reading_view = None
        self.categories:'list[Category]' = None
        self.selected_category:'Category' = None
        self.substituted_food:'Food' = None
        self.substitution_foods: 'list[SubstituteFood]' = None

    def run_data_initialization(self):
        """OFF search API data are : get, reorganized and inserted into the
        local database (for the moment, db is created by executing
        pur_beurre_db_creation.sql out of this python program)"""

        if self.args.load_data:
            if self.args.verbose:
                self.init_view.data_initialization_step(1)
            if self.args.page != self.init_view.page_arg_def_val:
                curr_responses_list = dt.get_off_api_data(self.args.page)
            else:
                curr_responses_list = dt.get_off_api_data(self.init_view.page_arg_def_val)
            if self.args.verbose:
                self.init_view.step_done()
            
            if not dt.check_off_data_gotten(curr_responses_list):
                self.init_view.no_data_initialization_error()
                exit()

            ########################################################
            mu.sort_write_json_resp_by_category(curr_responses_list)  # my json writing to check data... => to be deleted !
            ########################################################
            
            if self.args.verbose:
                self.init_view.data_initialization_step(2)
            curr_valid_products_list = dt.build_list_of_all_valid_products(
                curr_responses_list)
            if self.args.verbose:
                self.init_view.step_done()
            
            if self.args.verbose:
                self.init_view.data_initialization_step(3)
            dt.select_and_translate_products_categories(curr_valid_products_list)
            if self.args.verbose:
                self.init_view.step_done()
            
            ########################################################
            mu.write_valid_products(curr_valid_products_list)  # my json writing to check data... => to be deleted !
            ########################################################

            if self.args.verbose:
                self.init_view.data_initialization_step(4)
            insert_results_counts_dict = dbi.db_insert_all_products(curr_valid_products_list, dbc.db_connector, dbc.db_connection_activate)
            if self.args.verbose:
                self.init_view.step_done()
                self.init_view.data_loading_results(insert_results_counts_dict)

        else:
            self.init_view.no_data_initialization_asked_by_user()
    
    def is_user_input_valid(self, input_value: 'str or int', view) -> bool:
        return (input_value in view.general_valid_input
                or input_value in view.menu_valid_input)

    def check_user_input(self, input_value: 'str or int', view: 'MainMenuView or subclasses') -> 'str or int':
        while not self.is_user_input_valid(input_value, view):
            input_value = view.get_user_choice()
        return input_value

    def is_user_ask_to_quit(self, input_value: str) -> bool:
        return input_value in cfg.QUIT_INPUT

    def process_user_input(self, input_value: str, view: 'MainMenuView or subclasses'):
        print(input_value)
        if input_value.isdigit():
            input_value = int(input_value)
            print("dans if isdigit() ", input_value)
        checked_input_val = self.check_user_input(input_value, view)
        if self.is_user_ask_to_quit(checked_input_val):
            view.quit_msg()
            exit()
        else:
            return checked_input_val
        
    def run_main_menu(self):
        self.main_view.display_specific_menu()
        user_choice = self.process_user_input(self.main_view.get_user_choice(), self.main_view)
        if user_choice == 1:
            self.run_cat_choice_menu()
        elif user_choice == 2:
            self.run_bookmark_reading()

    def run_cat_choice_menu(self):
        # WHEN user choose main menu n°1 for the 1st time THEN all categories have to been gotten from db :
        if not self.categories:
            self.categories = Category.objects.get_all()
            self.cat_view = vw.CatView()
        if len(self.categories) == 0:
            self.cat_view.no_data_found_error()
            exit()
        else:
            self.cat_view.display_specific_menu(self.categories)
            user_choice = self.cat_view.check_user_input(self.cat_view.get_user_choice())
            if user_choice in cfg.RETURN_PREV_MENU_INPUT:
                self.run_main_menu()
            elif user_choice == -1:
                exit()
            else:
                self.selected_category = self.categories[int(user_choice)-1]
                self.run_food_choice_menu()
    
    def run_food_choice_menu(self):
        self.selected_category.foods_category = Food.objects.get_all_by_category(self.selected_category.id)
        if not self.food_view or self.food_view.selected_category_name != self.selected_category.name:  # if it is not a user menu return or if user returned but choose the same category twice in a row
            self.food_view = vw.FoodView()

        if len(self.selected_category.foods_category) == 0:
            self.food_view.no_data_found_error()
            self.run_cat_choice_menu()
        else:
            self.food_view.display_specific_menu(self.selected_category)
            user_choice = self.food_view.check_user_input(self.food_view.get_user_choice())
            if user_choice in cfg.RETURN_PREV_MENU_INPUT:
                self.run_cat_choice_menu()
            elif user_choice == -1:
                exit()
            else:
                self.run_sub_search(self.selected_category.foods_category[int(user_choice)-1])

    def run_sub_search(self, substituted_food:'Food'):
        # WHEN user choose a food, substitute research has to be done
        # EXCEPT IF if he choose a food twice in a row :
        if not self.substituted_food or self.substituted_food != substituted_food:
            self.substituted_food = substituted_food
            self.substituted_food.categories_food = Category.objects.get_all_by_food(self.substituted_food.id)
            self.substituted_food.stores_food = Store.objects.get_all_by_food(self.substituted_food.id)
            self.substitution_foods = Food.objects.get_all_by_ctc_and_nutriscore_better_than(self.substituted_food)
            self.sub_view = vw.SubstitutionView()

        if len(self.substitution_foods) > 0:
            self.sub_view.display_specific_menu(self.substituted_food)
            self.sub_view.substitution_winners(self.substituted_food, self.substitution_foods)
            self.run_bookmarking(self.substitution_foods)
        else:
            similar_foods = Food.objects.get_all_by_compared_to_category(self.substituted_food)
            self.sub_view.display_specific_menu(self.substituted_food)
            self.sub_view.foods_similar_to_substituted_food(self.substituted_food, similar_foods)
            self.sub_view.display_general_menu()
            user_choice = self.sub_view.check_user_input(self.sub_view.get_user_choice())
            if user_choice in cfg.RETURN_PREV_MENU_INPUT:
                self.run_food_choice_menu()
            elif user_choice == -1:
                exit()
        
    def run_bookmarking(self, substitution_foods: 'list[SubstitutionFood]'):
        self.bookmarking_view = vw.BookmarkingView()
        self.bookmarking_view.display_specific_menu(substitution_foods)

        user_choice = self.bookmarking_view.check_user_input(self.bookmarking_view.get_user_choice())
        if user_choice in cfg.RETURN_PREV_MENU_INPUT:
            self.run_food_choice_menu()
        elif user_choice in cfg.RETURN_MAIN_MENU_INPUT:
            self.run_main_menu()
        elif user_choice == -1:
            exit()
        else:
            bookmarked_substitution_food = substitution_foods[int(user_choice) - 1]
            new_bookmark_bool = Food.objects.save_bookmark(bookmarked_substitution_food.id, bookmarked_substitution_food.substituted_food.id)
            self.bookmarking_view.bookmarked_substitution(new_bookmark_bool, bookmarked_substitution_food)
            self.run_bookmarking(self.substitution_foods)
    
    def run_bookmark_reading(self):
        bookmarks = Food.objects.get_all_bookmarks_name_id()
        self.bookmark_reading_view = vw.ReadBookmarksView()
        self.bookmark_reading_view.display_specific_menu(bookmarks)

        user_choice = self.bookmark_reading_view.check_user_input(self.bookmark_reading_view.get_user_choice())
        print(self.bookmark_reading_view.menu_valid_input)
        while user_choice in self.bookmark_reading_view.menu_valid_input:
            substitution_food_to_display = bookmarks[int(user_choice)-1]
            self.bookmark_reading_view.bookmarked_substitution(new_bk=None,
                                                               substitution_food=Food.objects.get_one_bookmark_all_infos(substitution_food_to_display.id,
                                                                                                                         substitution_food_to_display.substituted_food.id))
            self.bookmark_reading_view.display_general_menu()
            user_choice = self.bookmark_reading_view.check_user_input(self.bookmark_reading_view.get_user_choice())
            print("dans while... ", self.bookmark_reading_view.menu_valid_input)

        if user_choice in cfg.RETURN_PREV_MENU_INPUT or user_choice in cfg.RETURN_MAIN_MENU_INPUT:
            self.run_main_menu()
        elif user_choice == -1:
            exit()
            