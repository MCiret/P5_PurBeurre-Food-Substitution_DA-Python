from foodsubstitution.views.food_view import FoodView
from foodsubstitution.models.food_model import Food
from .menu_control import MenuControl

class FoodControl(MenuControl):
    """ Next Menu of CatMenuControl """
    
    def __init__(self):
        super().__init__(FoodView())
    
    def run_menu(self, full_control: 'FullControl', user_input: int=None) -> 'int or str':
        """
        Calls his view to display and get user choice in the category's foods
        existing in the queried database.
        """
        if user_input:
            selected_category = full_control.categories[user_input - 1]
            if not full_control.selected_category or selected_category != full_control.selected_category:  # if it is not a user menu return or if user returned but choose the same category twice in a row
                full_control.selected_category = selected_category
                full_control.selected_category.foods_category = selected_category.foods_category = Food.objects.get_all_by_category(selected_category.id)
        else:  # else = when user chose to go back to this menu
            selected_category = full_control.selected_category
       
        if len(selected_category.foods_category) == 0:
            self.view.no_data_found_error()
            return 'r'
        else:
            self.view.display_specific_menu(selected_category)
            return self.check_user_input(self.view.get_user_choice())
    