"""Data handling (no database direct access)
Look OC Webinaire (T. Chappuis) "BD - AOO - Orga du code"
"""

from .food_model import Food
from dataclasses import dataclass, field  # https://realpython.com/python-data-classes/#more-flexible-data-classes


@dataclass
class SubstitutionFood(Food):
    """A Food object with same compared_to_category but better nutriscore than
    the substituted Food object (which has been selected by user)"""

    substituted_food: Food = field(default=None)
