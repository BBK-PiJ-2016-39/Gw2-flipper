import json
import urllib2

def init():

    global item_details_url, recipe_url, price_url, recipe_search_url
    recipe_url = 'https://api.guildwars2.com/v1/recipe_details.json?recipe_id=%s'
    price_url = 'https://api.guildwars2.com/v2/commerce/prices/%s'
    item_details_url = 'https://api.guildwars2.com/v2/items/%s'
    recipe_search_url ='https://api.guildwars2.com/v2/recipes/search?output=%s'

def search_recipe_by_output(item_id):
    """

    :param item_id: craftable item
    :return: ids of the recipes that craft the item
    """
    url = recipe_search_url%(','.join(item_ids),)
    recipe_id= json.load(urllib2.urlopen(url))

    return recipe_id

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