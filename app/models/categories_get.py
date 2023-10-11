import json

class Categories:
    
    list_of_categories = []

    def __init__(self):
        
        with open("app\models\categories.json") as category_read:
            self.list_of_categories = json.loads(category_read.read())
    
    def read_from_categories():
        with open("app\models\categories.json") as category_read:
            return json.loads(category_read.read())

    @classmethod    
    def get_all_categories_and_tags(self):
        if len(self.list_of_categories) == 0:
            self.list_of_categories = self.read_from_categories()
        return self.list_of_categories
    
    @classmethod    
    def get_category_names(self):
        if len(self.list_of_categories) == 0:
            self.list_of_categories = self.read_from_categories()
        return [category["name"] for category in self.list_of_categories]

    @classmethod
    def get_all_tags(self):
        if len(self.list_of_categories) == 0:
            self.list_of_categories = self.read_from_categories()
        all_tags = []
        for category in self.list_of_categories:
            if category['name'] == 'all':
                pass
            else:
                if type(category["tags"]) == list:
                    [all_tags.append(tags["name"]) for tags in category["tags"]]
        
        return all_tags

    @classmethod
    def get_all_tags_in_category(self,category_name):
        if len(self.list_of_categories) == 0:
            self.list_of_categories = self.read_from_categories()
        all_tags = []
        for category in self.list_of_categories:
            if category['name'] == 'all':
                pass
            else:
                if type(category["tags"]) == list and category["name"] == category_name:
                    [all_tags.append(tags["name"]) for tags in category["tags"]]
        
        return all_tags

