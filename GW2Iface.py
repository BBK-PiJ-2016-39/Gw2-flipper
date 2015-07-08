import json
import urllib2
import logging
from datetime import datetime
from time import sleep

__author__ = 'alex'

def init():
    global item_details_url, recipe_url, price_url, recipe_search_url, property_list
    recipe_url = 'https://api.guildwars2.com/v1/recipe_details.json?recipe_id=%s'
    price_url = 'https://api.guildwars2.com/v2/commerce/prices/%s'
    item_details_url = 'https://api.guildwars2.com/v2/items/%s'
    recipe_search_url ='https://api.guildwars2.com/v2/recipes/search?output=%s'
    property_list = {
        'item' : ['id', 'name', 'description', 'type', 'rarity', 'details'],
        'price' : {
            'sells' :['quantity', 'unit_price'],
            'buys' : ['quantity', 'unit_price']
        }
    }

class Item:

    def __init__(self, item_id):
        self.id = item_id
        self.prices = []

    def load_from_api(self):
        url = item_details_url%(self.id,)

        try:
            item_raw = json.load(urllib2.urlopen(url))
            for prop in property_list['item']:
                setattr(self, prop, item_raw.get(prop, ''))

        except Exception, e:
            logging.error(e)


class Price:
    def __init__(self, item_id):
        self.id = item_id

    def load_prices_from_api(self):
        url = price_url%(self.id,)

        try:
            prices_raw = json.load(urllib2.urlopen(url))
            prices_raw['date'] = datetime.utcnow()
            self.prices.append(prices_raw)

        except Exception, e:
            logging.error(e)


    def print_item(self):
        for prop in property_list['item']:
            logging.info('%s  : %s', prop, getattr(self, prop,''))

        for record in self.prices:
            logging.info('prices  : %s', record)
        logging.info('-----\n')

"""
logging.basicConfig(level=logging.DEBUG)
init()

item_ids = ['28445', '28446', '12345']
items = []
for item_id in item_ids:
    item = Item(item_id)

    item.load_from_api()
    sleep(1)

    item.load_prices_from_api()
    item.print_item()
"""