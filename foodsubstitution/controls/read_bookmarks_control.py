from foodsubstitution.views.read_bookmarks_view import ReadBookmarksView
from foodsubstitution.models.food_model import Food
from .menu_control import MenuControl

class ReadBookmarksControl(MenuControl):
    """ Controller for menu called if user choose '2' in 1st menu (MainMenuControl) """ 
    
    def __init__(self):
        super().__init__(ReadBookmarksView())
    
    def run_menu(self, full_control: 'FullControl', user_input: int=None) -> 'int or str':
        """
        Calls his view to display all bookmarked substitution foods existing in
        the queried database and get user choice to display all informations
        about one of these bookmarks.
        """
        bookmarks = Food.objects.get_all_bookmarks_name_id_nutriscore()
        self.view.display_specific_menu(bookmarks)

        user_choice = self.check_user_input(self.view.get_user_choice())
        while user_choice in self.view.menu_valid_input:
            substitution_food_to_display = bookmarks[user_choice - 1]
            substitution_food_to_display = Food.objects.get_one_bookmark_all_infos(substitution_food_to_display.id, substitution_food_to_display.substituted_food.id)
            self.view.bookmarked_substitution(new_bk=None,
                                              substitution_food=substitution_food_to_display)
            self.view.display_general_menu()
            user_choice = self.check_user_input(self.view.get_user_choice())

        return user_choice
            