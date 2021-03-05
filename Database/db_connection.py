"""Look OC Webinaire (T. Chappuis) 'BD - AOO - Orga du code'"""

from mysql import connector as db
import config as cfg

# db connection created out of any classes because we want only 1 connection
# for the entire application (no need 1 connection for each manager object..)
# like singleton pattern...
db_conn = db.connect(**cfg.DB_PARAM)