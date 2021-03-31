from foodsubstitution.views.cat_view import CatView
from foodsubstitution.models.category_model import Category
from .menu_control import MenuControl

class CatControl(MenuControl):
    """ Controller for menu called if user choose '1' in 1st menu (MainMenuControl) """
    
    def __init__(self):
        super().__init__(CatView())
    
    def run_menu(self, full_control: 'FullControl', user_input: int=None) -> 'int or str':
        """
        Calls his view to display and get user choice in the categories existing
        in the queried database.
        """

        categories = full_control.categories
        # IF user choose 1- in the main menu for the 1st time SO all categories have to been gotten from db :
        if not categories:
            full_control.categories = categories = Category.objects.get_all()

        if len(categories) == 0:
            self.view.no_data_found_error()
            return 'q'
        else:
            self.view.display_specific_menu(categories)
            return self.check_user_input(self.view.get_user_choice())
