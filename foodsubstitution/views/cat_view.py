import config as cfg
from foodsubstitution.views.main_menu_view import MainMenuView

class CatView(MainMenuView):
    """ View called by CatControl for terminal displayings """

    def __init__(self):
        super().__init__()
        self.general_menu += (cfg.GENERAL_MENU_VALID_INPUT_DICT["return"],)
        self.set_general_menu_input()  # quit and go back to previous menu

    def display_specific_menu(self, categories:'list[Category]'):
        assert(type(categories) is list)

        self.set_specific_valid_input(len(categories))
        print("\nDans quelle catégorie d'aliments souhaitez-vous rechercher un substitut ?\n")
        for i, cat in enumerate((cat.name for cat in categories)):
            print(f"{i+1} --> {cfg.PRETTY_PRINT_CATEGORY_DICT[cat].capitalize()}")
        print("")
        self.display_general_menu()

    def no_data_found_error(self):
        print("\n\n⚠ Aucune catégorie d'aliment n'a été trouvée.\n" 
              "Votre base de données locale semble vide...\n"
              "Avez-vous bien exécuté le programme avec l'argument -ld "
              "au moins une fois ?\n"
              "Consultez l'aide (--help) ou le fichier README.rst.\n\n")
