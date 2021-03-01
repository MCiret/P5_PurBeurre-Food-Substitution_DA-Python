import config as cfg
import json
import requests


def get_json_data_from_off_api() -> 'list of GET queries responses (dict)':

    # Build the GET queries with categories criterion (see config.py)
    # and fields filters (see config.py) which are useful to fill de database.
    get_queries_list = []
    for categories_dict in cfg.GET_QUERY_CATEGORIES_LIST:
        query_str = "https://fr.openfoodfacts.org/cgi/search.pl?action=process"
        for key in categories_dict:
            query_str += f"&tagtype_{key}=categories" \
                         f"&tag_contains_{key}=contains" \
                         f"&tag_{key}={categories_dict[key]}"
        query_str += "&fields="
        for field in cfg.QUERY_FIELDS_LIST:
            query_str += f"{field},"
        query_str += f"&page_size={cfg.NB_PROD}&json=true"
        get_queries_list.append(query_str)

    get_responses_json_list = []
    for query in get_queries_list:
        # Request to the Open Food Facts search API.
        r = requests.get(query, headers=cfg.GET_QUERY_HEADER)
        # Queries responses (json data) are loads in a dict.
        get_responses_json_list.append(json.loads(r.text))

    return get_responses_json_list


def sort_and_write_outfile_json_data(json_data_list: list):
    """Used to read GET queries responses and find data fields to extract
    for database filling"""
    assert(type(json_data_list) is list and len(json_data_list) != 0)

    get_out_files_names_list = []

    for categories_dict in cfg.GET_QUERY_CATEGORIES_LIST:
        out_file_name = "OFF API GET Queries Responses - sorted and filtered" \
                        "/response_get_query_category"
        for key in categories_dict:
            out_file_name += f"_{categories_dict[key]}"
        out_file_name += "_fields_filters.json"
        # out_file_name += ".json"
        get_out_files_names_list.append(out_file_name)

    for i in range(len(json_data_list)):
        with open(get_out_files_names_list[i], "w",
                  encoding="utf-8") as out_file:
            json.dump(json_data_list[i], out_file,
                      indent=4, sort_keys=True, ensure_ascii=False)


def make_list_of_all_valid_products(off_api_json_responses: list) -> list:
    """ Each response is a dict, where the "products" key is a list of
    food products, where each product is a 8 keys/fields dict.
    A valid product = has the 5 required fields (quantity and stores_tags are optional).
    => This function just appends each valid product dict in a list.
    """
    return [prod for resp_dict in off_api_json_responses
            for prod in resp_dict["products"]
            if "_id" in prod.keys()
            and "product_name" in prod.keys()
            and "nutriscore_grade" in prod.keys()
            and "url" in prod.keys()
            and "categories_tags" in prod.keys()
            and "compared_to_category" in prod.keys()
            ]


def select_and_translate_products_categories(json_products: list):
    """:param json_products is modified by side effect"""
    for prod_dict in json_products:
        tmp_categories_list = []
        for category in prod_dict["categories_tags"]:
            if category in cfg.CATEGORIES_TAGS_FR_TRANSLATION.keys():
                tmp_categories_list.append(cfg.CATEGORIES_TAGS_FR_TRANSLATION[category])
        prod_dict["categories_tags"] = tmp_categories_list
