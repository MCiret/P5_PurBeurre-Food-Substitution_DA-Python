GENERAL_MENU_VALID_INPUT_DICT = {
    "quit": {"val": ('q', 'Q'), "txt": "🖮  Q ou q : quitter"},
    "return": {"val": ('r', 'R'), "txt": "🖮  R ou r : retour au menu précédent"},
    "main": {"val": ('M', 'm'), "txt": "🖮  M ou m : menu principal"}
}

# Categories used in the GET queries to request Open Food Facts search API
GET_QUERY_LIST_CATEGORIES_DICT = [
    {"0": "desserts", "1": "biscuits"},
    {"0": "desserts", "1": "fromages"},
    {"0": "petit-dejeuners"},
    {"0": "boissons", "1": "eaux"},
    {"0": "boissons", "1": "sodas"},
    {"0": "viandes", "1": "plats_prepares", "2": "charcuteries"},
    {"0": "pizzas"},
]

GET_QUERY_HEADER = {'user-agent': 'P5_DAPython - Linux - v0 - no_url'}

NB_PROD_PER_PAGE = 50  # number of product per page gotten from OFF search API

# Fields filters used in the GET queries (request OFF data using API search)
# for recovering only usefull data for the database
QUERY_FIELDS_LIST = [
    "_id", "product_name", "quantity",
    "nutriscore_grade", "url",
    "stores_tags", "categories_tags", "compared_to_category"
]

# Categories which are kept for each product food gotten from OFF search API.
# And because they are often in english, it translates them to be used in this
# french version (application and database values).
CATEGORIES_TAGS_FR_TRANSLATION = {
    "en:desserts": "desserts",
    "en:biscuits": "biscuits",
    "en:cheeses": "fromages",
    "en:breakfasts": "petit-dejeuners",
    "en:beverages": "boissons",
    "en:waters": "eaux",
    "en:sodas": "sodas",
    "en:meats": "viandes",
    "en:meals": "plats_prepares",
    "en:prepared-meats": "charcuteries",
    "en:pizzas": "pizzas",
    "en:breads": "pains",
    "en:frozen-foods": "surgelés",
    "en:dairies": "produits laitiers",
    "fr:pates-a-tartiner": "pates-a-tartiner"  # category kept for db but already in french
}

PRETTY_PRINT_CATEGORY_DICT = {
    "desserts": "Desserts",
    "biscuits": "Biscuits",
    "fromages": "Fromages",
    "petit-dejeuners": "Petits-déjeuners",
    "boissons": "Boissons",
    "eaux": "Eaux",
    "sodas": "Sodas",
    "viandes": "Viandes",
    "plats_prepares": "Plats préparés",
    "charcuteries": "Charcuteries",
    "pizzas": "Pizzas",
    "pains": "Pains",
    "surgelés": "Surgelés",
    "produits laitiers": "Produits laitiers",
    "pates-a-tartiner": "Pâtes à tartiner"
}

# local database connection parameters #
DB_PARAM = {
    'user': 'root',
    'password': 'boutaz',
    'host': '127.0.0.1',
    'database': 'pur_beurre_db',  # see database_managers/pur_beurre_db.sql file
    'raise_on_warnings': True  # warnings should raise exceptions
}
