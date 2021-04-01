from foodsubstitution.views.bookmarking_view import BookmarkingView

class ReadBookmarksView(BookmarkingView):
    """ View called by ReadBookmarksControl for terminal displayings """

    def __init__(self):
        super().__init__()    

    def display_specific_menu(self, bookmarks:'list[SubstitutionFood]'):
        assert(type(bookmarks) is list)
        
        nb_bookmarks = len(bookmarks)
        super().set_specific_valid_input(nb_bookmarks)
        print(f"\n{'~'*179}")
        print(f"{'NUMÉRO':^10}{' ≀ ':^3}{'ALIMENT SUBSTITUÉ':^80}{' VS ':^4}{'ALIMENT SUBSTITUT':^80}{' ≀':>2}")
        print(f"{'~'*179}")
        for i, bk in enumerate(bookmarks):
            substituted_text = bk.substituted_food.name
            if bk.substituted_food.quantity:
                substituted_text += " (" + bk.substituted_food.quantity + ")"
            substituted_text += " > " + bk.substituted_food.nutriscore.capitalize() + " <"
            substitution_text = bk.name
            if bk.quantity:
                substitution_text += " (" + bk.quantity + ")"
            substitution_text += " > " + bk.nutriscore.capitalize() + " <"
            print(f"{i+1:^10}{' ≀ ':^3}{substituted_text:^80}{' VS ':^4}{substitution_text:^80}{' ≀':>2}")
            print(f"{'~'*179}")

        print(f"\n💾 Vous avez {nb_bookmarks} aliments substitués sauvegardés.\n"
               "    🛈 Un aliment est substitué par un aliment substitut (c'est à dire ayant un meilleur Nutri-Score).")

        if nb_bookmarks > 0:
            print("\n⮱ Saisir le numéro pour afficher plus d'informations.\n")
        else:
            print("\n⮱ Pour sauvegarder des aliments substitués, il vous faut effectuer une recherche de substituts (➔ Menu principal : 1- Quel aliment souhaitez-vous remplacer ?).\n")
        self.display_general_menu()
