"""Look OC Webinaire (T. Chappuis) 'BD - AOO - Orga du code'"""

from mysql import connector as db_connector
import config as cfg

# db connection created out of any classes because we want only 1 connection
# for the entire application (no need 1 connection for each manager object..)
# like singleton pattern...
try:
    db_connection_activate = db_connector.connect(**cfg.DB_PARAM)
except db_connector.ProgrammingError:
    print(f"La base de données {cfg.DB_PARAM['database']} n'existe pas.\n"
          f"Consulter le fichier README.rst, section 'Installation', étape 2. concernant la création de la base de données.\n"
          f"Exit...")
    exit()

