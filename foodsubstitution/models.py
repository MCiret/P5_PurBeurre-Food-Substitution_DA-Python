
@dataclass
class SubstitutionFood(Food):
    """A Food object with same compared_to_category but better nutriscore than
    the substituted Food object (which has been selected by user)"""

    substituted_food: Food = field(default=None)

@dataclass
class Category:

    objects = CategoryManager(db_connection_activate)  # Django style

    # id (PK in db) is not in init parameters because we don't want
    # to initialise it "by hand" => it has to be handle by managers..
    id: int = field(init=False, default=None)
    name: str = field(default=None)  # attribute not involved in tables relations
    foods_category: List[Food] = field(default=None)  # attribute involved in/representing tables relations

@dataclass
class Store:

    objects = StoreManager(db_connection_activate)  # Django style

    # id (PK in db) is not in init parameters because we don't want
    # to initialise it "by hand" => it has to be handle by managers..
    id: int = field(init=False, default=None)
    name: str = field(default=None)  # attribute not involved in tables relations
    foods_store: List[Food] = field(default=None)  # attribute involved in/representing tables relations
