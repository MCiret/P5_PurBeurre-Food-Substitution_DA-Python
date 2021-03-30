import config as cfg
import json
import requests


def get_off_api_data(page_nb: int) -> "list[dict]":

    # Build the GET queries to retrieve json data from OFF search API
    get_queries_list = []
    for categories_dict in cfg.GET_QUERY_LIST_CATEGORIES_DICT:
        query_str = "https://fr.openfoodfacts.org/cgi/search.pl?action=process"
        for key in categories_dict:
            query_str += f"&tagtype_{key}=categories" \
                         f"&tag_contains_{key}=contains" \
                         f"&tag_{key}={categories_dict[key]}"
        query_str += "&fields="
        for field in cfg.QUERY_FIELDS_LIST:
            query_str += f"{field},"
        query_str += f"&page_size={cfg.NB_PROD_PER_PAGE}" \
                     f"&page={page_nb}&json=true"  
        get_queries_list.append(query_str)

    responses_json_list = []
    for query in get_queries_list:
        # Requests the Open Food Facts (OFF) search API.
        r = requests.get(query, headers=cfg.GET_QUERY_HEADER)
        # Responses (json) are loads in a dict.
        responses_json_list.append(json.loads(r.text))
        
    return responses_json_list


def check_off_data_gotten(off_api_json_responses:'list[dict[dict]]') -> 'list[dict]':
    """A valid product has to be formed with 6 of the 8 requested fields
    ("stores_tags" and "quantity_product" are optional)."""

    nb_query_resp_ok = 0
    for resp in off_api_json_responses:
        nb_query_resp_ok += len(resp["products"])

    return nb_query_resp_ok != 0 


def build_list_of_all_valid_products(off_api_json_responses:
                                     'list[dict[dict]]') -> 'list[dict]':
    """A valid product has to be formed with 6 of the 8 requested fields
    ("stores_tags" and "quantity_product" are optional)."""

    return [prod for resp_dict in off_api_json_responses
            for prod in resp_dict["products"]
            if "_id" in prod.keys()
            and "product_name" in prod.keys()
            and "nutriscore_grade" in prod.keys()
            and "url" in prod.keys()
            and "categories_tags" in prod.keys()
            and "compared_to_category" in prod.keys()
            ]


def select_and_translate_products_categories(valid_products: 'list[dict]'):
    """To have french categories names in database.
    The list is modified by side effect."""
    for prod in valid_products:
        tmp_categories_list = []
        for category in prod["categories_tags"]:
            if category in cfg.CATEGORIES_TAGS_FR_TRANSLATION.keys():
                tmp_categories_list.append(cfg.CATEGORIES_TAGS_FR_TRANSLATION[category])
        prod["categories_tags"] = tmp_categories_list
