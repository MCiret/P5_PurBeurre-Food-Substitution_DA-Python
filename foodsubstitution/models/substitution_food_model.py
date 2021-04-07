from .food_model import Food
from dataclasses import dataclass, field


@dataclass
class SubstitutionFood(Food):
    """
    It is a Food object with an added attribute : the substituted food (i.e selected by user)
    which have the same compared_to_category but a worse nutriscore
    """

    substituted_food: Food = field(default=None)
