from foodsubstitution.views.cat_view import CatView
from foodsubstitution.models.category_model import Category
from .menu_control import MenuControl

class CatControl(MenuControl):
    
    def __init__(self):
        super().__init__(CatView())
    
    def run_menu(self, full_control: 'FullControl', user_input: int=None):
        categories = full_control.categories
        # WHEN user choose main menu n°1 for the 1st time THEN all categories have to been gotten from db :
        if not categories:
            full_control.categories = categories = Category.objects.get_all()

        if len(categories) == 0:
            self.view.no_data_found_error()
            return 'q'
        else:
            self.view.display_specific_menu(categories)
            return self.check_user_input(self.view.get_user_choice())
