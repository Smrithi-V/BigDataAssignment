from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client.telephone_billing

# Load data from Excel
customers_df = pd.read_excel('customers.xlsx')
calls_df = pd.read_excel('calls.xlsx')
rates_df = pd.read_excel('rates.xlsx')

# Insert data into MongoDB collections
db.customers.insert_many(customers_df.to_dict('records'))
db.calls.insert_many(calls_df.to_dict('records'))
db.rates.insert_many(rates_df.to_dict('records'))
