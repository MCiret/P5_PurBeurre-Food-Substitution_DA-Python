from foodsubstitution.views.main_menu_view import MainMenuView
from .menu_control import MenuControl

class MainMenuControl(MenuControl):
    
    def __init__(self):
        super().__init__(MainMenuView())   

    def run_menu(self, full_control: 'FullControl', user_input=None):
        self.view.display_specific_menu()
        return self.check_user_input(self.view.get_user_choice())
