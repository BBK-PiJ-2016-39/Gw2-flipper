__author__ = 'Alex'

#!/usr/bin/python
import json
import urllib2

def init():

    global item_details_url, recipe_url, price_url, recipe_search_url
    recipe_url = 'https://api.guildwars2.com/v1/recipe_details.json?recipe_id=%s'
    price_url = 'https://api.guildwars2.com/v2/commerce/prices/%s'
    item_details_url = 'https://api.guildwars2.com/v2/items/%s'
    recipe_search_url ='https://api.guildwars2.com/v2/recipes/search?output=%s'

class Item:
   'Common base class for all employees'
   Count = 0

   def __init__(self, item_id):
        url = item_details_url%(item_id,)

        try:
            item = json.load(urllib2.urlopen(url))

            props = ['name', 'type', 'description']
            for prop in props:
                if prop in item:
                    setattr(self, prop, item[prop])
                else:
                    setattr(self, prop, None)

            Item.Count += 1
        except Exception:
            print 'Error'

   def display_item(self):
        if self.Count:
            print "Name : ", self.name
            print "Description : ", self.description
            print "Type : ", self.type


"""
def get_item_tree(self):
    recipe_list = api_call
        for recipe in recipe_list:
            items = get_items_for_recipe
            for item in items:
                item.get_item_tree()
"""

init()
"This would create first object of Employee class"
emp1 = Item('2845')
"This would create second object of Employee class"
#emp2 = Employee('5')
emp1.display_item()
#emp2.displayEmployee()

item_ids = ['28445', '28446', '28447']
items = []
for item_id in item_ids:
    item = Item(item_id)
    items.append(item)
    item.display_item()