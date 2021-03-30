from foodsubstitution.views.substitution_view import SubstitutionView
from foodsubstitution.models.food_model import Food
from foodsubstitution.models.category_model import Category
from foodsubstitution.models.store_model import Store
from .menu_control import MenuControl

class SubstitutionControl(MenuControl):
    
    def __init__(self):
        super().__init__(SubstitutionView())
    
    def run_menu(self, full_control: 'FullControl', user_input: int=None):
        if user_input:
            substituted_food = full_control.selected_category.foods_category[user_input - 1]
            # WHEN user choose a food, substitute research has to be done
            # EXCEPT IF if he choose a food twice in a row :
            if not full_control.substituted_food or substituted_food != full_control.substituted_food:
                full_control.substituted_food = substituted_food
                full_control.substituted_food.categories_food = substituted_food.categories_food = Category.objects.get_all_by_food(substituted_food.id)
                full_control.substituted_food.stores_food = substituted_food.stores_food = Store.objects.get_all_by_food(substituted_food.id)
                full_control.substitution_foods = substitution_foods = Food.objects.get_all_by_ctc_and_nutriscore_better_than(substituted_food)
            else:
                substitution_foods = full_control.substitution_foods 
        else:  # else = user returns back in menus
            substituted_food = full_control.substituted_food
            substitution_foods = full_control.substitution_foods
        
        if len(substitution_foods) > 0:
            self.view.display_specific_menu(substituted_food)
            self.view.substitution_winners(substitution_foods)
            return 0
        else:
            similar_foods = Food.objects.get_all_by_compared_to_category(substituted_food.id, substituted_food.compared_to_category)
            self.view.display_specific_menu(substituted_food)
            self.view.foods_similar_to_substituted_food(substituted_food, similar_foods)
            self.view.display_general_menu()
            return self.check_user_input(self.view.get_user_choice())
