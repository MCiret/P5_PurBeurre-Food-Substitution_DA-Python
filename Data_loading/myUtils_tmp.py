import json
import config as cfg


def sort_write_json_resp_by_category(off_api_json_responses: 'list[dict[dict]]'):
    """GET queries responses from OFF search API"""
    assert(type(off_api_json_responses) is list and len(off_api_json_responses) != 0)

    get_out_files_names_list = []

    for categories_dict in cfg.GET_QUERY_LIST_CATEGORIES_DICT:
        out_file_name = "Data_loading/Written json data" \
                        "/response_get_query_category"
        for key in categories_dict:
            out_file_name += f"_{categories_dict[key]}"
        out_file_name += "2.json"
        get_out_files_names_list.append(out_file_name)

    for i in range(len(off_api_json_responses)):
        with open(get_out_files_names_list[i], "w",
                  encoding="utf-8") as out_file:
            json.dump(off_api_json_responses[i], out_file,
                      indent=4, sort_keys=True, ensure_ascii=False)


def write_valid_products(valid_products: 'list[dict]'):
    with open("Written json data/final_products2.json", "a",
              encoding="utf-8") as of:
        json.dump(valid_products, of,
                  indent=4, sort_keys=True, ensure_ascii=False)