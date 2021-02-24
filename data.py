from mysql import connector as db
import config as cfg
import json
import requests


def get_json_data_from_off_api() -> 'list of GET query response (dict)':

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
        for field in cfg.JSON_DATABASE_FIELDS_DICT:
            query_str += f"{field},"
        query_str += "&page_size=50&json=true"
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
        out_file_name = "response_get_query_category"
        for key in categories_dict:
            out_file_name += f"_{categories_dict[key]}"
        out_file_name += "_fields_filters.json"
        get_out_files_names_list.append(out_file_name)

    for i in range(len(json_data_list)):
        with open(get_out_files_names_list[i], "w", encoding="utf-8") as out_file:
            json.dump(json_data_list[i], out_file, indent=4, sort_keys=True, ensure_ascii=False)


curr_responses_list = get_json_data_from_off_api()


def database_connection(db_connection_param: dict) -> 'database connector':
    return db.connect(db_connection_param)