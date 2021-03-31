from foodsubstitution.views.food_view import FoodView

class SubstitutionView(FoodView):
    """ View called by SubstitutionControl for terminal displayings """

    def __init__(self):
        super().__init__()
        
    def display_specific_menu(self, substituted_food: 'Food'):
        self.set_specific_valid_input(0)  # this class only displays then the bookmarking view is directly called
        print(f"\n{'⊰⊱ ALIMENT SUBSTITUÉ ⊰⊱':^150}")
        super().display_one_food_in_array(substituted_food)

    def explain_substitution_results(self):    
        print("\n🛈 Précisions sur les résultats :\n"
              "∙ Substitué = aliment à substituer.\n"
              "∙ Substitut = même sous-catégorie de comparaison que l'aliment substitué et un meilleur nutriscore.\n"
              "∙ Similaire = uniquement même sous-catégorie de comparaison que l'aliment substitué (affiché(s) uniquement si aucun substitut n'a été trouvé).")

    def foods_similar_to_substituted_food(self, substituted_food:'Food', similar_foods:' list[Food]'):
        """ Display when no substitution food has been found"""
        tot_nb_sim_food = len(similar_foods)
        txt1 = "⚠ Aucun substitut n'a été trouvé pour **"+f"{substituted_food.name}"+"**.\n"
        txt2 = "🛈 Votre base de donnée locale ne contient peut-être pas assez de données ou l'aliment sélectionné présente un bon Nutri-Score."
        txt3 = "⮱ Consultez l'aide (README.rst ou --help) pour alimenter votre base de données locale.\n"

        for i, sim_food in enumerate(similar_foods):
            print(f"\n{'⊰ Aliment similaire n°'+str(i+1)+'/'+str(tot_nb_sim_food)+' ⊱':^150}")
            super().display_one_food_in_array(sim_food)
        print(f"\n{'↑ '+str(tot_nb_sim_food)+' ALIMENT(S) SIMILAIRES ONT ÉTÉ TROUVÉS ↑':^150}")
        self.explain_substitution_results()
        print(f"\n\n{txt1:^150}")
        print(f"{txt2:^150}")
        print(f"{txt3:^150}")

    def substitution_winners(self, substitution_foods:'list[SubstitutionFood]'):
        """ Display when at lest 1 substitution food has been found"""
        tot_nb_found_substitute = len(substitution_foods)
        print("")
        for i, sub in enumerate(substitution_foods):
            print(f"\n{'⊰ Substitut n°'+str(i+1)+'/'+str(tot_nb_found_substitute)+' ⊱':^150}")
            super().display_one_food_in_array(sub)
        print(f"\n\n{'🔍🔍    ↑ '+str(tot_nb_found_substitute)+' ALIMENT(S) SUBSTITUTS ONT ÉTÉ TROUVÉS ↑    🔍🔍':^150}\n")
        self.explain_substitution_results()
