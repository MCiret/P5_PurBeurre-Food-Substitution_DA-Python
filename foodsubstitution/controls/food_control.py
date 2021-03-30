from foodsubstitution.views.food_view import FoodView
from foodsubstitution.models.food_model import Food
from .menu_control import MenuControl

class FoodControl(MenuControl):
    
    def __init__(self):
        super().__init__(FoodView())
    
    def run_menu(self, full_control: 'FullControl', user_input: int=None):
        if user_input:
            selected_category = full_control.categories[user_input - 1]
            if not full_control.selected_category or selected_category != full_control.selected_category:  # if it is not a user menu return or if user returned but choose the same category twice in a row
                full_control.selected_category = selected_category
                full_control.selected_category.foods_category = selected_category.foods_category = Food.objects.get_all_by_category(selected_category.id)
        else:  # else = user returns back in menus
            selected_category = full_control.selected_category
       
        if len(selected_category.foods_category) == 0:
            self.view.no_data_found_error()
            return 'r'
        else:
            self.view.display_specific_menu(selected_category)
            return self.check_user_input(self.view.get_user_choice())
    
