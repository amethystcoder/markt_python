import json


def read_from_categories():
    with open("app\models\categories.json") as category_read:
        return json.loads(category_read.read())


def get_all_categories_and_tags():
    list_of_categories = []
    if len(list_of_categories) == 0:
        list_of_categories = read_from_categories()
    return list_of_categories


def get_category_names(list_of_categories):
    if len(list_of_categories) == 0:
        list_of_categories = read_from_categories()
    return [category["name"] for category in list_of_categories]


def get_all_tags():
    list_of_categories = []
    if len(list_of_categories) == 0:
        list_of_categories = read_from_categories()
    all_tags = []
    for category in list_of_categories:
        if category['name'] == 'all':
            pass
        else:
            if type(category["tags"]) == list:
                [all_tags.append(tags["name"]) for tags in category["tags"]]

    return all_tags


def get_all_tags_in_category(category_name):
    list_of_categories = []
    if len(list_of_categories) == 0:
        list_of_categories = read_from_categories()
    all_tags = []
    for category in list_of_categories:
        if category['name'] == 'all':
            pass
        else:
            if type(category["tags"]) == list and category["name"] == category_name:
                [all_tags.append(tags["name"]) for tags in category["tags"]]

    return all_tags
