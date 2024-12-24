import pandas as pd
from pymongo import MongoClient
from datetime import datetime

customers_df = pd.read_excel('customers.xlsx')
calls_df = pd.read_excel('calls.xlsx')
rates_df = pd.read_excel('rates.xlsx')

client = MongoClient('mongodb://localhost:27017/')
db = client['telephone_company']

db.customers.delete_many({}) 
db.calls.delete_many({})      
db.rates.delete_many({})      

db.customers.insert_many(customers_df.to_dict('records'))
db.calls.insert_many(calls_df.to_dict('records'))
db.rates.insert_many(rates_df.to_dict('records'))


def generate_report(customer_id):
    customer = db.customers.find_one({'customer_id': customer_id})
    calls = list(db.calls.find({'customer_id': customer_id}))
    rate = db.rates.find_one({'rate_id': 1}) 

    report = {
        'Customer Information': {
            'Name': customer['name'],
            'Address': customer['address'],
            'Phone Number': customer['phone_number']
        },
        'Call History': [],
        'Billing Summary': {
            'Total Calls': len(calls),
            'Total Duration': 0,
            'Total Cost': 0
        }
    }

    total_duration = 0
    total_cost = 0

    for call in calls:
        duration_in_minutes = call['duration'] / 60
        cost = duration_in_minutes * rate['cost_per_minute']
        total_duration += duration_in_minutes
        total_cost += cost

        report['Call History'].append({
            'Date': call['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
            'Duration': round(duration_in_minutes, 2),
            'Cost': round(cost, 2)
        })

    report['Billing Summary']['Total Duration'] = round(total_duration, 2)
    report['Billing Summary']['Total Cost'] = round(total_cost, 2)

    return report

def print_report(report):
    print("Customer Information")
    print("====================")
    print(f"Name: {report['Customer Information']['Name']}")
    print(f"Address: {report['Customer Information']['Address']}")
    print(f"Phone Number: {report['Customer Information']['Phone Number']}")
    print("\nCall History")
    print("============")
    for call in report['Call History']:
        print(f"Date: {call['Date']}")
        print(f"Duration: {call['Duration']} minutes")
        print(f"Cost: ${call['Cost']}")
        print("------------")
    print("\nBilling Summary")
    print("================")
    print(f"Total Calls: {report['Billing Summary']['Total Calls']}")
    print(f"Total Duration: {report['Billing Summary']['Total Duration']} minutes")
    print(f"Total Cost: ${report['Billing Summary']['Total Cost']}")
    print("\n" + "="*30 + "\n")

all_customers = db.customers.find()
reports = []

for customer in all_customers:
    customer_id = customer['customer_id']
    report = generate_report(customer_id)
    reports.append(report)

for report in reports:
    print_report(report)