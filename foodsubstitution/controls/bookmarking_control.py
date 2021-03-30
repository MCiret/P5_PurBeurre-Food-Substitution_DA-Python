from foodsubstitution.views.bookmarking_view import BookmarkingView
from foodsubstitution.models.food_model import Food
from .menu_control import MenuControl

class BookmarkingControl(MenuControl):
    
    def __init__(self):
        super().__init__(BookmarkingView())
    
    def run_menu(self, full_control: 'FullControl', user_input: int=None):
        substitution_foods = full_control.substitution_foods
        self.view.display_specific_menu(substitution_foods)

        user_choice = self.check_user_input(self.view.get_user_choice())
        while user_choice in self.view.menu_valid_input:  # if user chooses to bookmark one of the substitution
            bookmarked_substitution_food = substitution_foods[user_choice - 1]
            new_bookmark_bool = Food.objects.save_bookmark(bookmarked_substitution_food.id, bookmarked_substitution_food.substituted_food.id)
            self.view.bookmarked_substitution(new_bookmark_bool, bookmarked_substitution_food)
            self.view.display_specific_menu(substitution_foods)
            user_choice = self.check_user_input(self.view.get_user_choice())
        

        return user_choice
