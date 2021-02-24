# from mysql import connector as db
import config as cfg
import json, requests

# conn = db.connect()


def get_json_data_from_off_api() -> 'list of GET query response (dict)':

    # Build the GET queries with categories criterion (see config.py)
    # and fields filters (see config.py) which are useful to fill de database.
    get_queries_list = []
    for categories_dict in cfg.DATA_CATEGORIES_LIST:
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

    # for query in get_queries_list:
    #     print(query)

    get_responses_json_list = []
    for query in get_queries_list:
        # Request to the Open Food Facts search API.
        r = requests.get(query, headers=cfg.GET_QUERY_HEADER)
        # Queries responses (json data) are loads in a dict.
        get_responses_json_list.append(json.loads(r.text))

    return get_responses_json_list


def tmp_outfile_sort_and_write_json_data(json_data_list: list):
    """
    Temporary function, just to see sorted queries response in a file
    --> TO DELETE LATER...
    :param json_data_list:
    :return:
    """
    assert(type(json_data_list) is list and len(json_data_list) != 0)

    get_out_files_names_list = []

    for categories_dict in cfg.DATA_CATEGORIES_LIST:
        out_file_name = "response_get_query_category"
        for key in categories_dict:
            out_file_name += f"_{categories_dict[key]}"
        out_file_name += "_fields_filters.json"
        get_out_files_names_list.append(out_file_name)

    for i in range(len(json_data_list)):
        with open(get_out_files_names_list[i], "w", encoding="utf-8") as out_file:
            json.dump(json_data_list[i], out_file, indent=4, sort_keys=True, ensure_ascii=False)


def tmp_write_keys_by_keys(json_responses_list, out_file_name, key):

    nb_resp = 0
    with open(out_file_name, "w", encoding="utf-8") as of:
        for resp in json_responses_list:
            of.write("================== QUERY RESPONSE ==================\n")
            nb_resp += 1
            nb_prod = 0
            for product in resp["products"]:
                nb_prod += 1
                of.write(f"~~~~~~~~~~ Resp n°{nb_resp} - Product n°{nb_prod} ~~~~~~~~~~\n")
                of.write("barcode --> ")
                of.write(product["_id"])
                if type(product[key]) is list:
                    of.write(f"\n{key} : \n")
                    for elem in product[key]:
                        of.write(elem)
                        of.write("\n")
                else:
                    of.write(f"\n{key} --> ")
                    of.write(product[key])
                of.write("\nproduct_name --> ")
                of.write(product["product_name"])
                of.write("\n")
            of.write("====================================================\n")


curr_responses_list = get_json_data_from_off_api()
tmp_outfile_sort_and_write_json_data(curr_responses_list)
# tmp_write_keys_by_keys(curr_responses_list, "keys_compared_to_category.txt", "compared_to_category")
# tmp_write_keys_by_keys(curr_responses_list, "keys_categories_tags.txt", "categories_tags")


######## [toKeep] my JSON tests ########
# json.loads() to obtain a dict from the json r.text
# json.dumps(...) to indent and sort but it returns a str
# r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=petit-dejeuners&page_size=20&json=true")
# data_dict = json.loads(r.text)
# with open("s2.json", "w", encoding="utf-8") as out_file:
#     json.dump(data_dict, out_file, indent=4, sort_keys=True, ensure_ascii=False)




