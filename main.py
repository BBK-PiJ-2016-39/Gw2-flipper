1
from functions import *
#import functions.py


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