from database_managers.category_manager import CategoryManager
from database_managers.db_connection import db_connection_activate, db_connector
from dataclasses import dataclass, field


@dataclass
class Category:
    """Category objects initialized in database SELECT queries"""

    objects = CategoryManager(db_connection_activate, db_connector)

    id: int = field(init=False, default=None)
    name: str = field(default=None)
    foods_category: 'list[Food]' = field(default=None)  # representing tables relations
