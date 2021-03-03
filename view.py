import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Pur Beurre - Food substitution application",
                                     epilog="See README.rst (USAGE section) and/or directly the OFF API documentation for more details about the GET query configuration.")
    parser.add_argument("-ld", "--load_data", action="store_true", help="Get data from OFF search API to insert them in the locale database.")
    parser.add_argument("-p", "--page", default=1, help="The page number to get from OFF search API (default = 1 and the -ld argument is required).")

    args = parser.parse_args()
    return args


def display_data_loading_step(code: int):
    if code == 1:
        print(f"Step {code} : GET data from OFF search API...", end="")
    elif code == 2:
        print(f"Step {code} : Parse responses and build one list "
              f"with all valid products...", end="")
    elif code == 3:
        print(f"Step {code} : Selection and translation of categories...", end="")
    elif code == 4:
        print(f"Step {code} : Products inserting in the local database...", end="")


def display_no_data_loading():
    print("No data loading asked...\n"
          "You are going to use Pur Beurre Food substitution application "
          "with the actual local database.")


def display_done_msg():
    print("Done.")


def display_db_insertions_counts(db_insertions_counters: dict):
    print(f"Products to insert = {db_insertions_counters['to_insert']}\n"
          f"Products inserted = {db_insertions_counters['prod']}\n"
          f"Categories inserted = {db_insertions_counters['cat']}\n"
          f"Stores inserted = {db_insertions_counters['store']}")
