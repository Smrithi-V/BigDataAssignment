import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Generate Customers Data
customers = []
for i in range(1, 51):
    customers.append([i, fake.name(), fake.address(), fake.phone_number()])

customers_df = pd.DataFrame(customers, columns=["customer_id", "name", "address", "phone_number"])
customers_df.to_excel("customers.xlsx", index=False)

# Generate Calls Data
calls = []
for i in range(1, 201):
    customer_id = random.randint(1, 50)
    timestamp = fake.date_time_this_year()
    duration = random.randint(1, 3600)
    cost = random.choice([0.05, 0.03, 0.02])
    calls.append([i, customer_id, timestamp, duration, cost])

calls_df = pd.DataFrame(calls, columns=["call_id", "customer_id", "timestamp", "duration", "cost"])
calls_df.to_excel("calls.xlsx", index=False)

# Generate Rates Data
rates = [
    [1, "Standard Rate", 0.05],
    [2, "Evening Rate", 0.03],
    [3, "Weekend Rate", 0.02]
]

rates_df = pd.DataFrame(rates, columns=["rate_id", "description", "cost_per_minute"])
rates_df.to_excel("rates.xlsx", index=False)

print("Data generated and saved to Excel files successfully.")
