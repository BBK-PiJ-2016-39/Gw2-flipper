__author__ = 'alex'

import schedule
import time
from datetime import datetime
import json
import urllib2
import logging

from pymongo import MongoClient

def init():

    global mdb
    mng = MongoClient('localhost')
    mdb = mng['gw2flipper']

    global item_ids
    item_ids = ['28445', '28446', '12345', '19684', '19709',
                '36200', '36179', '36190', '36183', '36180',
                '19741', '19745', '19718', '19743', '19748',
                '19739'
                ]

    global stats_keys
    stats_keys = [
        'item_id', 'day_hour',
        'n_prc',
        'buys_avg_up', 'buys_avg_q',
        'sells_avg_up', 'sells_avg_q'
    ]

    global price_url
    price_url = 'https://api.guildwars2.com/v2/commerce/prices?ids=%s'

    logging.basicConfig(level=logging.DEBUG)



def prices_stats_average(a,n,b):
    return (a * n + b)/(n+1)

def prices_stats_give_time():
    return str(datetime.today().weekday()) + '_' + str(datetime.today().hour)



def prices_stats_init(item_id):
    """
    receives item_id
    retreives from mongo statistic with item_id and time
    :param item_id:
    :return: initialized price to be processed
    """

    id = int(item_id)
    stats_from_mongo = mdb.hourlyStats.find_one({'item_id' : id, 'day_hour' : prices_stats_give_time()})

    price_stats ={}
    for key in stats_keys:
        price_stats[key] = stats_from_mongo[key] \
            if stats_from_mongo is not None \
            else 0

    return price_stats

def prices_update_stats(stats, api_price):

    stats['buys_avg_up'] = prices_stats_average(stats['buys_avg_up'], stats['n_prc'], api_price['buys']['unit_price'])
    stats['buys_avg_q'] = prices_stats_average(stats['buys_avg_q'], stats['n_prc'], api_price['buys']['quantity'])
    stats['sells_avg_up'] = prices_stats_average(stats['sells_avg_up'], stats['n_prc'], api_price['buys']['unit_price'])
    stats['sells_avg_q'] = prices_stats_average(stats['sells_avg_q'], stats['n_prc'], api_price['buys']['quantity'])

    stats['item_id'] = api_price['id']
    stats['day_hour'] = prices_stats_give_time()
    stats['n_prc'] += 1

    logging.info('Updated stats for item: %s', stats['item_id'])
    return stats


def prices_load():

    logging.info('Loading prices at %s ...', datetime.utcnow())

    start_time = time.time()

    bulk_price = mdb.TPData.initialize_unordered_bulk_op()
    bulk_stats = mdb.hourlyStats.initialize_unordered_bulk_op()

    url = price_url%(','.join(item_ids))
    try:
        prices_raw = json.load(urllib2.urlopen(url))
        end_time = time.time()
        logging.info('Queried URL in %s seconds', (end_time-start_time))

        for price in prices_raw:
            price['date_time'] = datetime.utcnow()

            stats = prices_stats_init(price['id'])
            new_stats = prices_update_stats(stats, price)

            bulk_price.insert(price)
            bulk_stats.find({'item_id' : price['id'] , 'day_hour' : prices_stats_give_time()}).\
                upsert().replace_one(new_stats)

        bulk_price.execute()
        bulk_stats.execute()

    except Exception, e:
        logging.error(e)


    end_time = time.time()
    logging.info('Loaded prices for %d items in %s seconds', len(item_ids), end_time-start_time)


def main():
    # schedule.every(1).minutes.do(load_prices)
    '''
    schedule.every(1).hour.do(prices_load)

    while True:
        schedule.run_pending()
        time.sleep(1)
    '''

    prices_load()

def run():
    init()
    main()

if __name__ == '__main__':
    run()

