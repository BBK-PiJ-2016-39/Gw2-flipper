import json
import urllib2

def init():

    global recipe_url
    recipe_url = "https://api.guildwars2.com/v1/recipe_details.json?recipe_id=%s"

def get_recipe(item_ids):

    url = recipe_url%(','.join(item_ids),)
    recipe = json.load(urllib2.urlopen(url))
    import pdb; pdb.set_trace()

    return recipe

init()
recipe = get_recipe(['1275', '1276'])
print recipe['ingredients']

for item in recipe['ingredients']:
    print item['item_id'] + "  " + item['count']
    price = json.load(urllib2.urlopen("https://api.guildwars2.com/v2/commerce/prices/" + item['item_id']))
    print (int(price['sells']['unit_price']) * int(item['count']))