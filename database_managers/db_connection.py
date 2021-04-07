from mysql import connector as db_connector
import config as cfg

try:
    db_connection_activate = db_connector.connect(**cfg.DB_PARAM)
except db_connector.ProgrammingError as err:
    print(f"\nUn problème est survenu lors de la connexion à la base de données {cfg.DB_PARAM['database']}.")
    if err.errno == 1045:
        print("Vérifier les paramètres de connexion dans le fichier config.py du projet.\n")
    elif err.errno == 1049:
        print("La base de données n'existe pas. Consulter le fichier README.rst, section 'Installation', "
              "étape 2. concernant la création de la base de données.\n")
    else:
        print(f"{err}")
    print("Exit...")
    exit()
