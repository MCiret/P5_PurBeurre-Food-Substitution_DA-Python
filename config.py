### Open Food Facts (OFF) data ###

# Categories used in the GET queries to request OFF data using API search
GET_QUERY_CATEGORIES_LIST = [
    {"0": "desserts", "1": "biscuits"},
    {"0": "desserts", "1": "fromages"},
    {"0": "petit-dejeuners"},
    {"0": "boissons", "1": "eaux"},
    {"0": "boissons", "1": "sodas"},
    {"0": "viandes", "1": "plats_prepares", "2": "charcuteries"},
    {"0": "pizzas"},
]

GET_QUERY_HEADER = {'user-agent': 'P5_DAPython - Linux - v0 - no_url'}

# Fields filters used in the GET queries (request OFF data using API search)
# for recovering only datas then used in the database
# {json field: database field (table.field)}
JSON_DATABASE_FIELDS_DICT = {
    "_id": "food.barcode",
    "product_name": "food.product",
    "nutriscore_grade": "food.nutri_score",
    "url": "food.url_openfoodfacts",
    "stores_tags": "store.name",
    "categories_tags": "category.name"
}

# The field "Categories_tags" values (in json data) are often in english
# whereas the database and the application have to be in french
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
    "en:dairies": "produits laitiers"
}

### Open Food Facts (OFF) data ###

DB_CONFIG = {
    'user': 'root',
    'password': 'boutaz',
    'host': '127.0.0.1',
    'database': 'pur_beurre_off_db',
     'raise_on_warnings': True  # warnings should raise exceptions
}
