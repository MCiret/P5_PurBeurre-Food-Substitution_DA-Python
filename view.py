import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("ld", type=str, help="load data : enter Y/y to get data from Open Food Facts API and fill the local database OR enter N/n if your local database contains data.")
    args = parser.parse_args()
    return args


def display_args_error_msg(arg: str):
    print(f"The 'ld' argument value should be Y/y ou N/n."
          f"You have entered {arg}. Exit...")


def display_data_loading_step(code: int):
    if code == 1:
        print(f"Step {code} : GET data from OFF API...", end="")
    elif code == 2:
        print(f"Step {code} : Parse responses and build one list"
              f"with all valid products...", end="")
    elif code == 3:
        print(f"Step {code} : Keep some chosen categories"
              f"and translate them...", end="")
    elif code == 4:
        print(f"Step {code} : Fill the local database...", end="")
    elif code == 5:
        print("You have informed that your local database contains data.\n"
              "=> Ready to use the Pur Beurre Food substitution application.")


def display_done_msg():
    print("Done.")