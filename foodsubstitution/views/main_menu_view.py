import config as cfg

class MainMenuView:

    def __init__(self):
        self.general_menu = (cfg.GENERAL_MENU_VALID_INPUT_DICT["quit"],)
        self.set_general_menu_input()
    
    def set_general_menu_input(self):
        self.general_valid_input = ()
        for menu_dict in self.general_menu:
            if menu_dict["val"] not in self.general_valid_input:
                self.general_valid_input += menu_dict["val"]

    def set_specific_valid_input(self, nb_items: int):
        if nb_items == 0:
            self.menu_valid_input = ()  # empty tuple
        else:
            self.menu_valid_input = tuple(range(1, nb_items+1))

    def display_general_menu(self):
        for menu_dict in self.general_menu:
            print(menu_dict["txt"])

    def display_specific_menu(self):
        self.set_specific_valid_input(2)
        print("\n\n⊰⊰⊰⊰⊰⊰⊰⊰⊰⊰⊰⊰⊰⊰⊰⊰⊰ . ⊱⊱⊱⊱⊱⊱⊱⊱⊱⊱⊱⊱⊱⊱⊱⊱\n"
              "⊰⊰ Pur Beurre - Food Substitution ⊱⊱\n"
              "         ~ French version ~\n\n")
        print("1 - Quel aliment souhaitez-vous remplacer ?\n"
              "2 - Retrouver mes aliments substitués.\n")
        self.display_general_menu()
 
    def get_user_choice(self) -> str:
        user_choice = input("\nVeuillez saisir votre choix : ")
        if user_choice.isdigit():
            return int(user_choice)
        else:
            return user_choice
    
    def quit_msg(self):
        print("Exit...")
    