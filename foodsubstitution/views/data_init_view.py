import argparse
import config as cfg


class DataInitView:
    """
    View called by DataInitControl for command-line arguments parsing,
    displayings if user enters --verbose argument and potential error/problem
    during data initialization.
    """

    def __init__(self):
        self.page_arg_def_val = 1

    def get_run_args(self):
        parser = argparse.ArgumentParser(description="Pur Beurre - Food substitution application",
                                         epilog="See README.rst (USAGE section) and/or directly the OFF API documentation for more details about the GET query configuration.")
        parser.add_argument("-ld", "--load_data", action="store_true", help="Get data from OFF search API to insert them in the locale database.")
        parser.add_argument("-p", "--page", default=self.page_arg_def_val, help="The page number to get from OFF search API (default = 1 and the -ld argument is required).")
        parser.add_argument("-v", "--verbose", action="store_true", help="Details about data loading are displayed (steps and data loading results details).")
        args = parser.parse_args()
        return args
    
    def data_initialization_step(self, code):
        if code == 1:
            print(f"Step {code} : GET data from OFF search API page n°{self.page_arg_def_val}...", end="", flush=True)
        elif code == 2:
            print(f"Step {code} : Parse responses and build one list "
                  f"with all valid products...", end="", flush=True)
        elif code == 3:
            print(f"Step {code} : Selection and translation of categories...", end="", flush=True)
        elif code == 4:
            print(f"Step {code} : Products inserting in the local database... ⌛", end="", flush=True)
    
    def step_done(self):
        print("Done.")

    def no_data_initialization_asked_by_user(self):
        print("No data initialization or adding to the actual database...\n"
              "You are going to use Pur Beurre Food substitution application "
              "with the actual data set.\n\n")
    
    def no_data_initialization_error(self):
        print("\n⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠\n"
              "⚠ Get queries responses are empty = no data were retrieved from OFF search API.\n"
              "⚠ Unless you would have modify something, the problem comes from the OFF database.\n"
              "⚠ Please try again later...\n"
              "⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠⚠\n"
              "Exit...")
    
    def data_loading_results(self, db_insertions_counters: dict):
        print(f"\n>>>>>>>>>> Data loading results <<<<<<<<<<\n"
              f"Step 1 : Food products gotten from OFF search API = {db_insertions_counters['to_insert']}\n"
              f"Step 4 : New Foods inserted in local db = {db_insertions_counters['prod']}\n"
              f"Step 4 : New Categories inserted in local db = {db_insertions_counters['cat']}\n"
              f"Step 4 : New Stores inserted in local db = {db_insertions_counters['store']}\n"
              f"\n🛈  Step 1 upper than 0 but one of Step 4 = 0 means that GET queries to OFF search API have found products which have been already inserted in the local database.\n")
