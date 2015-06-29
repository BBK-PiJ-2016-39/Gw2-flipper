import json
import urllib2

def init():

    global item_details_url, recipe_url, price_url
    recipe_url = 'https://api.guildwars2.com/v1/recipe_details.json?recipe_id=%s'
    price_url = 'https://api.guildwars2.com/v2/commerce/prices/%s'
    item_details_url = 'https://api.guildwars2.com/v2/items/%s'

def get_item_details(item_ids):
    """
    Obtains details about an item (description, type, raryity etc)
    :param item_ids:
    :return:
    """
    url = item_details_url%(','.join(item_ids),)
    item = json.load(urllib2.urlopen(url))

    return item

def get_recipe(item_ids):
    """

    :param item_ids: items id
    :return:    returns
    """
    url = recipe_url%(','.join(item_ids),)
    recipe = json.load(urllib2.urlopen(url))
    #import pdb; pdb.set_trace()

    return recipe

def get_price(item_ids):
    """

    :param item_ids:    items id
    :return:    returns bid price
    """
    url = price_url%(','.join(item_ids),)
    price = json.load(urllib2.urlopen(url))
    if price['sells']['unit_price']:
        return price['sells']['unit_price']
    else:
        return '0'

def is_craftable(item_id):

    """
    Checks if item is craftable
    :param item_id: item id
    :return:    if not craftable returns 0, otherwise returns recipe ID
    """
    return 1


init()

input = raw_input("Enter something: ")

recipe = get_recipe([input])

print 'output item id: ' + recipe['output_item_id']
print 'output item name' + get_item_details([recipe['output_item_id']])['name']
print recipe['ingredients']

total = 0

for item in recipe['ingredients']:

    print get_item_details([item['item_id']])['name'] + "  " + item['count']
    price = get_price([item['item_id']])

    if int(price):
        print (int(price) * int(item['count']))
        total +=(int(price) * int(item['count']))
    else:
        print 'item not tradable'

print 'Total price to craft: ' + str(total)
#print (int(get_price(['46738'])) * 0.85)