__author__ = 'alex'

# 1) Connect to a MongoDB document collection
# 2) Insert a document
# 3) Display all of the documents in a collection

from pymongo import MongoClient

connection = MongoClient("localhost:27017")

# connect to the db and collection
db = connection.test.inputs

# create dictionary
test_record = {}

# set flag variable
flag = True

# loop for data input
bulk_test = db.initialize_unordered_bulk_op()

while (flag):
  test_name,test_number = raw_input("Enter name and number: ").split(',')
  test_record = {'name':test_name,'number':test_number}
  bulk_test.insert(test_record)
  flag = raw_input('Enter another record? y/N ')
  if (flag[0].upper() == 'N'):
     flag = False

bulk_test.execute()

# find all documents
results = db.find()

print('')
print('-----')

# display documents from collection
for record in results:
# print out the document
  print(record)

print('')

# close the connection to MongoDB
connection.close()
