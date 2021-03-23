import argparse
import config as cfg


class DataInitView:

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
              f"Food products gotten from OFF search API = {db_insertions_counters['to_insert']}\n"
              f"New Foods inserted in local db = {db_insertions_counters['prod']}\n"
              f"New Categories inserted in local db = {db_insertions_counters['cat']}\n"
              f"New Stores inserted in local db = {db_insertions_counters['store']}\n")


class MainMenuView:

    def __init__(self):
        self.general_valid_input = cfg.QUIT_INPUT
        self.menu_valid_input = cfg.MAIN_MENU_VALID_INPUT

    def display_general_menu(self):
        print("🖮  Q ou q : quitter")

    def display_specific_menu(self):
        print("\n\n⊰⊰⊰⊰⊰⊰⊰⊰⊰⊰⊰⊰⊰⊰⊰⊰⊰ . ⊱⊱⊱⊱⊱⊱⊱⊱⊱⊱⊱⊱⊱⊱⊱⊱\n"
              "⊰⊰ Pur Beurre - Food Substitution ⊱⊱\n"
              "         ~ French version ~\n\n")
        print("1 - Quel aliment souhaitez-vous remplacer ?\n"
              "2 - Retrouver mes aliments substitués.\n")
        self.display_general_menu()
 
    def get_user_choice(self) -> str:
        return(input("\nVeuillez saisir votre choix de menu : "))
    
    def is_user_input_valid(self, input_value: str) -> bool:
        try:
            return (input_value in self.general_valid_input
                    or input_value in self.menu_valid_input
                    or int(input_value) in self.general_valid_input
                    or int(input_value) in self.menu_valid_input)
        except ValueError:
            return False
    
    def is_user_ask_to_quit(self, input_value: str) -> bool:
        return input_value in cfg.QUIT_INPUT

    def check_user_input(self, input_value):
        while not self.is_user_input_valid(input_value):
            input_value = self.get_user_choice()
        if self.is_user_ask_to_quit(input_value):
            print("Exit...")
            return -1
        else:
            return input_value


class CatView(MainMenuView):

    def __init__(self, nb_categories: int=-1):
        super().__init__()
        self.general_valid_input += cfg.RETURN_PREV_MENU_INPUT
        if nb_categories != -1:  # else = when it is called in subclasses FoodView or ReadBookmarksView so all categories are useless
            self.menu_valid_input = tuple(range(1, nb_categories+1))

    def display_general_menu(self):
        super().display_general_menu()
        print("🖮  R ou r : retour au menu précédent")

    def display_specific_menu(self, categories:'list[Category]'):
        print("\nDans quelle catégorie d'aliments souhaitez-vous rechercher un substitut ?\n")
        for i, cat in enumerate((cat.name for cat in categories)):
            print(f"{i+1} --> {cfg.PRETTY_PRINT_CATEGORY_DICT[cat].capitalize()}")
        print("")
        self.display_general_menu()

    def get_user_choice(self) -> str:
        return(input("\nVeuillez saisir votre choix de catégorie : "))

    def no_data_found_error(self):
        print("\n\n⚠ Aucune catégorie d'aliment n'a été trouvée.\n" 
              "Votre base de données locale semble vide...\n"
              "Avez-vous bien exécuté le programme avec l'argument -ld "
              "au moins une fois ?\n"
              "Consultez l'aide (--help) ou le fichier README.rst.\n\n"
              "Exit...")


class FoodView(CatView):
    
    def __init__(self, selected_category_name: str=None, nb_foods_in_selected_category: int=-1):
        super().__init__()
        if selected_category_name:  # else = when it is called in subclass SubstituteView so selected category is useless
            self.menu_valid_input = tuple(range(1, nb_foods_in_selected_category+1))
            self.selected_category_name: str = selected_category_name

    def display_specific_menu(self, foods_in_selected_category: 'list[Food]'):
        print(f"\n⮱ Pour quel(le) {cfg.PRETTY_PRINT_CATEGORY_DICT[self.selected_category_name].capitalize()} souhaitez-vous rechercher un substitut ?\n")
        for i, food in enumerate(foods_in_selected_category):
            print(f"{i+1} --> {food.name}", end="")
            if food.quantity:
                print(f" ({food.quantity})")
            else:
                print("")
        print("")
        self.display_general_menu()
    
    def get_user_choice(self) -> str:
        return(input(f"\nVeuillez saisir votre choix d'aliment {self.selected_category_name.capitalize()} : "))
    
    def display_one_food_in_array(self, food:'Food'):
        print(f"{'~'*150}")
        print(f"{'≀ ':<2}{food.name+' ('+food.quantity+')':^146}{' ≀':>2}")
        print(f"{'~'*150}")
        print(f"{'≀':<1}{' Code Barre ':^24}{'≀ ':<2}{food.id:^121}{' ≀':>2}")
        print(f"{'~'*150}")
        print(f"{'≀':<1}{' Nutri-Score ':^24}{'≀ ':<2}{food.nutriscore.upper():^121}{' ≀':>2}")
        print(f"{'~'*150}")
        print(f"{'≀':<1}{' Open Food Facts URL ':^24}{'≀ ':<2}{food.url_openfoodfacts:^121}{' ≀':>2}")
        print(f"{'~'*150}")
        self.display_food_category_or_store_in_array("Catégorie(s)", food.categories_food)
        self.display_food_category_or_store_in_array("Magasin(s)", food.stores_food)
                
    def display_food_category_or_store_in_array(self, array_row_name: str, cat_or_store: 'list[Category or Store]'):
            whole_str = ""
            print(f"{'≀ ':<2}{array_row_name:^22}{' ≀':>2}", end="")
            if len(cat_or_store) == 0:
                print(f"{'Non Renseigné':^122}{' ≀':>2}")
                print(f"{'~'*150}")
            else:
                for i, elem in enumerate(cat_or_store):
                    if elem.name in cfg.PRETTY_PRINT_CATEGORY_DICT.keys():
                        whole_str += cfg.PRETTY_PRINT_CATEGORY_DICT[elem.name].capitalize()
                    else:
                        whole_str += elem.name.capitalize()
                    if i+1 < len(cat_or_store):
                        whole_str += " ∙ "
                print(f"{whole_str:^122}{' ≀':>2}")
                print(f"{'~'*150}")

    def no_data_found_error(self):
        print(f"\n\n⚠ Aucun aliment n'a été trouvé dans la catégorie "
              f"{cfg.PRETTY_PRINT_CATEGORY_DICT[self.selected_category_name].capitalize()}.\n" 
              f"Consultez l'aide (README.rst ou --help) pour alimenter votre base de données locale\n."
              f"Retour au menu précédent...\n")


class SubstitutionView(FoodView):
    
    def substituted_food(self, substituted_food:'Food'):
        print(f"\n{'⊰⊱ ALIMENT À SUBSTITUER ⊰⊱':^150}")
        self.display_one_food_in_array(substituted_food)

    def explain_substitution_results(self):    
        print("\n🛈 Précisions sur la recherche de substitut :\n"
              "∙ Substitut = même sous-catégorie de comparaison que l'aliment à substituer et un meilleur nutriscore.\n"
              "∙ Similaire = uniquement même sous-catégorie de comparaison que l'aliment à substituer (affiché(s) uniquement si aucun substitut n'a été trouvé).")

    def foods_similar_to_substituted_food(self, substituted_food:'Food', similar_foods:' list[Food]'):
        self.substituted_food(substituted_food)
        tot_nb_sim_food = len(similar_foods)
        txt1 = "⚠ Aucun substitut n'a été trouvé pour **"+f"{substituted_food.name}"+"**.\n"
        txt2 = "🛈 Votre base de donnée locale ne contient peut-être pas assez de données ou l'aliment sélectionné présente un Nutri-Score assez élevé."
        txt3 = "⮱ Consultez l'aide (README.rst ou --help) pour alimenter votre base de données locale.\n"

        print(f"\n{'⊰⊱ '+str(tot_nb_sim_food)+' ALIMENT(S) SIMILAIRES ⊰⊱':^150}")
        for i, sim_food in enumerate(similar_foods):
            print(f"\n{'⊰ Aliment similaire n°'+str(i+1)+'/'+str(tot_nb_sim_food)+' ⊱':^150}")
            self.display_one_food_in_array(sim_food)
        self.explain_substitution_results()
        print(f"\n\n{txt1:^150}")
        print(f"{txt2:^150}")
        print(f"{txt3:^150}")
        self.display_general_menu()

    def substitution_winners(self, substituted_food:'Food', substitution_foods:'list[SubstituteFood]'):
        self.substituted_food(substituted_food)
        tot_nb_found_substitute = len(substitution_foods)
        print(f"\n{'⊰⊱ '+str(tot_nb_found_substitute)+' ALIMENT(S) SUBSTITUTS TROUVÉS ⊰⊱':^150}")
        for i, sub in enumerate(substitution_foods):
            print(f"\n{'⊰ Substitut n°'+str(i+1)+'/'+str(tot_nb_found_substitute)+' ⊱':^150}")
            self.display_one_food_in_array(sub)
        self.explain_substitution_results()

    def display_specific_menu(self):
        print("\n\n💾 Saisir le numéro (n°) d'un substitut pour le sauvegarder et pouvoir le consulter ultérieurement (➔ Menu principal 2- Retrouver mes aliments substitutés).\n")
        self.display_general_menu()

    def get_user_choice(self) -> str:
        return(input("\nVeuillez saisir votre choix : "))

class BookmarkingView(SubstitutionView):

    def __init__(self, sub_view_valid_input):
        super().__init__()
        self.general_valid_input += cfg.RETURN_MAIN_MENU_INPUT
        self.menu_valid_input = sub_view_valid_input

    def display_general_menu(self):
        super().display_general_menu()
        print("🖮  M ou m : menu principal")

    def display_specific_menu(self):
        print("\n💾 Saisir le numéro (n°) d'un autre substitut de la recherche précédente pour le sauvegarder.\n")
        self.display_general_menu()
    
    def bookmarked_substitution(self, new_bk: bool, substitution_food:'SubstitutionFood'):
        print(f"{'~'*200}")
        print(f"{'≀':<1}{' Bookmarked ':^35}{'≀ ':<2}{'Aliment substitut':^78}{' VS ':^4}{'Aliment substitué':^78}{' ≀':>2}")
        print(f"{'~'*200}")
        print(f"{'≀':<1}{' Aliment ':^35}{'≀ ':<2}{substitution_food.name+' ('+substitution_food.quantity+')':^78}{' VS ':^4}{substitution_food.substituted_food.name+' ('+substitution_food.substituted_food.quantity+')':^78}{' ≀':>2}")
        print(f"{'~'*200}")
        print(f"{'≀':<1}{' Nutri-Score ':^35}{'≀ ':<2}{substitution_food.nutriscore.upper():^78}{' VS ':^4}{substitution_food.substituted_food.nutriscore.upper():^78}{' ≀':>2}")
        print(f"{'~'*200}")
        print(f"{'≀':<1}{' Open Food Facts URL (substitut) ':^35}{'≀ ':<2}{substitution_food.url_openfoodfacts:^160}{' ≀':>2}")
        print(f"{'~'*200}")
        print(f"{'≀':<1}{' Open Food Facts URL (substitué) ':^35}{'≀ ':<2}{substitution_food.substituted_food.url_openfoodfacts:^160}{' ≀':>2}")
        print(f"{'~'*200}")
        print(f"{'≀':<1}{' Magasin(s) (substitut) ':^35}{'≀ ':<2}", end="")
        whole_str = ""
        if len(substitution_food.stores_food) == 0:
            print(f"{'Non Renseigné':^160}{' ≀':>2}")
            print(f"{'~'*200}")
        else:
            for i, store in enumerate(substitution_food.stores_food):
                whole_str += store.name.capitalize()
                if i+1 < len(substitution_food.stores_food):
                    whole_str += " ∙ "
            print(f"{whole_str:^160}{' ≀':>2}")
            print(f"{'~'*200}")

        if new_bk == 1:
            print("\n\n⮱ Le substitut sélectionné a été sauvegardé dans votre base de données locale 🗹")
        else:
            print("\n\n🛈 Le substitut sélectionné a déjà été sauvegardé dans votre base de données locale...")

class ReadBookmarksView(CatView):

    def __init__(self, nb_bookmarks: int):
        super().__init__()
        self.menu_valid_input = tuple(range(1, nb_bookmarks + 1))

    def display_specific_menu(self, bookmarks:'list[SubstitutionFood]'):
        for i, bk in enumerate(bookmarks):
            print(f"{i+1}) {bk.name}", end="")
            if bk.quantity:
                print(f" ({bk.quantity})", end="")
            print(f" est un substitut de {bk.substituted_food.name}", end="")
            if bk.substituted_food.quantity:
                print(f" ({bk.quantity})")
            else:
                print("")
        print("")
        print(f"\n⮱ Vous avez {len(bookmarks)} aliments substitués sauvegardés.\n"
               "    ⮱ Saisir le numéro d'un aliment substituté pour afficher plus d'informations.\n")
        self.display_general_menu()

    def get_user_choice(self) -> str:
        return(input("\nVeuillez saisir votre choix : "))

    
