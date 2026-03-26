import pandas as pd
from sqlalchemy import create_engine

# DB connection
DB_USER = "postgres"
DB_PASSWORD = "Tiyanka10??"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "mavenflix_dw"

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Load staging data
staging_df = pd.read_csv("data/staging/cleaned_subscriptions.csv")

# Convert Yes/No to 1/0
staging_df['was_subscription_paid'] = staging_df['was_subscription_paid'].map({'Yes':1, 'No':0})

# ------------------------
# CUSTOMER DIMENSION
# ------------------------
# Only customer_id available
customer_dim = staging_df[['customer_id']].drop_duplicates()
customer_dim.to_sql("dim_customer", engine, if_exists="replace", index=False)

# ------------------------
# SUBSCRIPTION DIMENSION
# ------------------------
subscription_dim = staging_df[['subscription_cost', 'subscription_interval', 'subscription_length_days']].drop_duplicates()
subscription_dim['subscription_id'] = range(1, len(subscription_dim) + 1)  # surrogate key
subscription_dim.to_sql("dim_subscription", engine, if_exists="replace", index=False)

# ------------------------
# FACT TABLE
# ------------------------
# Merge subscription_dim to get subscription_id
fact_df = staging_df.merge(subscription_dim, on=['subscription_cost', 'subscription_interval', 'subscription_length_days'], how='left')
fact_df = fact_df[['customer_id', 'subscription_id', 'created_date', 'canceled_date', 'was_subscription_paid', 'is_active']]
fact_df.to_sql("fact_subscription", engine, if_exists="replace", index=False)

print("Data mart loaded successfully!")