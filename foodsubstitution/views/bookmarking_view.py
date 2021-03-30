import config as cfg
from foodsubstitution.views.substitution_view import SubstitutionView

class BookmarkingView(SubstitutionView):

    def __init__(self):
        super().__init__()
        self.general_menu += (cfg.GENERAL_MENU_VALID_INPUT_DICT["main"],)
        self.set_general_menu_input()

    def display_specific_menu(self, substitution_foods: 'list[SubstitutionFood]'):
        super().set_specific_valid_input(len(substitution_foods))
        print("\n\n💾 Saisir le numéro d'un substitut pour le sauvegarder et pouvoir le consulter ultérieurement (➔ Menu principal : 2- Retrouver mes aliments substitutés).\n")
        self.display_general_menu()
    
    def bookmarked_substitution(self, new_bk: bool, substitution_food:'SubstitutionFood'):
        print(f"\n{'~'*200}")
        print(f"{'≀':<1}{' SAUVEGARDE ':^35}{'≀ ':<2}{'ALIMENT SUBSTITUT':^78}{' VS ':^4}{'ALIMENT SUBSTITUÉ':^78}{' ≀':>2}")
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

        if new_bk == True:
            print("\n\n⮱ Le substitut sélectionné a été sauvegardé dans votre base de données locale 🗹")
        elif new_bk == False:
            print("\n\n🛈 Le substitut sélectionné est déjà sauvegardé dans votre base de données locale...")
        else:
            pass

