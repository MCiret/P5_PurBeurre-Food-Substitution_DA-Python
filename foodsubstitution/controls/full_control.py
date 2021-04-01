from .data_init_control import DataInitControl
from .menu_control import MenuControl
from .main_menu_control import MainMenuControl
from .cat_control import CatControl
from .food_control import FoodControl
from .substitution_control import SubstitutionControl
from .bookmarking_control import BookmarkingControl
from .read_bookmarks_control import ReadBookmarksControl
import config as cfg

class FullControl:
    """ Manages all menus controllers"""
    
    ATTRIBUTE_STR_TO_MENU_CONTROL_CLASS_DICT = {
        "main_menu_control": {"ct_class": "MainMenuControl", "next": ["cat_menu_control", "read_bookmarks_menu_control"]},
        "cat_menu_control": {"ct_class": "CatControl", "next": ["food_menu_control"], "prev": ["main_menu_control"]},
        "food_menu_control": {"ct_class": "FoodControl", "next": ["sub_menu_control"], "prev": ["cat_menu_control"]},
        "sub_menu_control": {"ct_class": "SubstitutionControl", "next": ["bookmarking_menu_control"], "prev": ["food_menu_control"]},
        "bookmarking_menu_control": {"ct_class": "BookmarkingControl", "prev": ["food_menu_control"]},
        "read_bookmarks_menu_control": {"ct_class": "ReadBookmarksControl", "prev": ["main_menu_control"]}
    }

    def __init__(self):
        # menus views controlers (instanced only if user asks)
        self.main_menu_control = MainMenuControl()
        self.cat_menu_control = None
        self.food_menu_control = None
        self.sub_menu_control = None
        self.bookmarking_menu_control = None
        self.read_bookmarks_menu_control = None
        # temporary data (i.e specific to the current user session)
        self.categories: 'list[Category]' = None
        self.selected_category: 'Category' = None
        self.substituted_food: 'Food' = None
        self.substitution_foods: 'list[SubstitutionFood]' = None

    def full_run(self):
        """The main function (called in main)"""
        
        DataInitControl.run_data_initialization()
        self.call_menu_control("main_menu_control")
    
    def call_menu_control(self, menu_control_name: 'str', user_input: 'int or str'=None):
        assert(type(menu_control_name) is str)
        
        if not getattr(self, menu_control_name):
            setattr(self, menu_control_name, globals()[FullControl.ATTRIBUTE_STR_TO_MENU_CONTROL_CLASS_DICT[menu_control_name]["ct_class"]]())
        checked_user_input = getattr(self, menu_control_name).run_menu(self, user_input)
        if checked_user_input in cfg.GENERAL_MENU_VALID_INPUT_DICT["quit"]["val"]:
            getattr(self, menu_control_name).view.quit_msg()
            exit()
        elif checked_user_input in cfg.GENERAL_MENU_VALID_INPUT_DICT["return"]["val"]:
            self.call_menu_control(FullControl.ATTRIBUTE_STR_TO_MENU_CONTROL_CLASS_DICT[menu_control_name]["prev"][0])
        elif checked_user_input in cfg.GENERAL_MENU_VALID_INPUT_DICT["main"]["val"]:
            self.call_menu_control("main_menu_control", checked_user_input)
        else:
            if menu_control_name == "main_menu_control":
                self.call_menu_control(FullControl.ATTRIBUTE_STR_TO_MENU_CONTROL_CLASS_DICT[menu_control_name]["next"][checked_user_input - 1] , checked_user_input)
            else:
                self.call_menu_control(FullControl.ATTRIBUTE_STR_TO_MENU_CONTROL_CLASS_DICT[menu_control_name]["next"][0] , checked_user_input)
    