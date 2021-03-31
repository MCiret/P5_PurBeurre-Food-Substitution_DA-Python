import config as cfg
from foodsubstitution.views.cat_view import CatView

class FoodView(CatView):
    """ View called by FoodControl for terminal displayings """

    def __init__(self):
        super().__init__()

    def display_specific_menu(self, selected_category: 'Category'):
        self.selected_category_name: str = selected_category.name
        super().set_specific_valid_input(len(selected_category.foods_category))
        print(f"\n⮱ Pour quel(le) {cfg.PRETTY_PRINT_CATEGORY_DICT[self.selected_category_name].capitalize()} souhaitez-vous rechercher un substitut ?\n"
               "   * aliment dont le nutriscore est déjà au maximum (A).\n")
        for i, food in enumerate(selected_category.foods_category):
            if food.nutriscore == 'a':
                food_name_txt = "*" + food.name
            else:
                food_name_txt = food.name
            print(f"{i+1:>4}{' --> ':^6}{food_name_txt}", end="")
            if food.quantity:
                print(f" ({food.quantity})")
            else:
                print("")
        print("\n* aliment dont le nutriscore est déjà au maximum (A).\n")
        super().display_general_menu()
    
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
