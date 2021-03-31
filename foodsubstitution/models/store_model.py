from database_managers.store_manager import StoreManager
from database_managers.db_connection import db_connection_activate, db_connector
from dataclasses import dataclass, field

@dataclass
class Store:
    """Store objects initialized in database SELECT queries"""

    objects = StoreManager(db_connection_activate, db_connector)

    id: int = field(init=False, default=None)
    name: str = field(default=None)
    foods_store: 'list[Food]' = field(default=None)  # representing tables relations
