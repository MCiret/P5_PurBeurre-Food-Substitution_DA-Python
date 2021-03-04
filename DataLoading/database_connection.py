"""Look OC Webinaire (T. Chappuis) 'BD - AOO - Orga du code'"""

from mysql import connector as db
import config as cfg

# db connection created out of any classes because we want 1 connection for
# for all the application (no need 1 connection for each manager object..
db_conn = db.connect(**cfg.DB_PARAM)