class MenuControl:
    """
    Base class for all menus controllers.
    Each menu controller is associated to one menu view.
    """

    def __init__(self, view):
        self.view = view

    def is_user_input_valid(self, input_value: 'str or int') -> bool:
        assert(type(input_value) is int or type(input_value) is str)

        return (input_value in self.view.general_valid_input
                or input_value in self.view.menu_valid_input)

    def check_user_input(self, input_value: 'str or int') -> 'str or int':
        assert(type(input_value) is int or type(input_value) is str)

        while not self.is_user_input_valid(input_value):
            input_value = self.view.get_user_choice()
        return input_value
