"""Look OC Webinaire (T. Chappuis) 'BD - AOO - Orga du code'"""

from mysql import connector as db_connector
import config as cfg

# db connection created out of any classes because we want only 1 connection
# for the entire application (no need 1 connection for each manager object..)
# like singleton pattern...
db_connection_activate = db_connector.connect(**cfg.DB_PARAM)

