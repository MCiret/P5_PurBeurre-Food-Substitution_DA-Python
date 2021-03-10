import argparse


class RunView:

    def __init__(self):
        self.page_arg_def_val = 1

    def get_run_args(self):
        parser = argparse.ArgumentParser(description="Pur Beurre - Food substitution application",
                                         epilog="See README.rst (USAGE section) and/or directly the OFF API documentation for more details about the GET query configuration.")
        parser.add_argument("-ld", "--load_data", action="store_true", help="Get data from OFF search API to insert them in the locale database.")
        parser.add_argument("-p", "--page", default=self.page_arg_def_val, help="The page number to get from OFF search API (default = 1 and the -ld argument is required).")

        args = parser.parse_args()
        return args
    
    def data_initialization_step(self, code):
        if code == 1:
            print(f"Step {code} : GET data from OFF search API page n°{self.page_arg_def_val}...", end="")
        elif code == 2:
            print(f"Step {code} : Parse responses and build one list "
                  f"with all valid products...", end="")
        elif code == 3:
            print(f"Step {code} : Selection and translation of categories...", end="")
        elif code == 4:
            print(f"Step {code} : Products inserting in the local database...", end="")
    
    def step_done(self):
        print("Done.")

    def no_data_initialization(self):
        print("No data initialization or adding to the actual database...\n"
              "You are going to use Pur Beurre Food substitution application "
              "with the actual data set.")

    def data_loading_results(self, db_insertions_counters: dict):
        print(f"Products to insert = {db_insertions_counters['to_insert']}\n"
              f"Products inserted = {db_insertions_counters['prod']}\n"
              f"Categories inserted = {db_insertions_counters['cat']}\n"
              f"Stores inserted = {db_insertions_counters['store']}")

class Welcome:
    
    def __init__(self):
        pass
