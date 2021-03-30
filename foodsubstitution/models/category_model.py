"""Data handling (no database direct access)
Look OC Webinaire (T. Chappuis) "BD - AOO - Orga du code"
"""

from database_managers.category_manager import CategoryManager
from database_managers.db_connection import db_connection_activate, db_connector
from dataclasses import dataclass, field  # https://realpython.com/python-data-classes/#more-flexible-data-classes

@dataclass
class Category:

    objects = CategoryManager(db_connection_activate, db_connector)  # Django style

    # id (PK in db) is not in init parameters because we don't want
    # to initialise it "by hand" => it has to be handle by managers..
    id: int = field(init=False, default=None)
    name: str = field(default=None)  # attribute not involved in tables relations
    foods_category: 'list[Food]' = field(default=None)  # attribute involved in/representing tables relations
