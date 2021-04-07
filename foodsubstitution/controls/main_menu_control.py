from foodsubstitution.views.main_menu_view import MainMenuView
from .menu_control import MenuControl


class MainMenuControl(MenuControl):
    """
    First menu controller
    """

    def __init__(self):
        super().__init__(MainMenuView())

    def run_menu(self, full_control: 'FullControl', user_input=None) -> 'int or str':
        """
        Calls his view to display and get user choice between the two main
        menus :
        1- Food substitution research ;
        2- Boorkmarked Food substitutions displaying ;
        """
        self.view.display_specific_menu()
        return self.check_user_input(self.view.get_user_choice())
