import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# DB connection
DB_USER = "postgres"
DB_PASSWORD = "Tiyanka10??"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "mavenflix_dw"

# URL-encode the password to handle special characters
DB_PASSWORD_ENCODED = quote_plus(DB_PASSWORD)

# Create SQLAlchemy engine
engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Load cleaned data
df = pd.read_csv("data/staging/cleaned_subscriptions.csv")

# Optional: Convert Yes/No to 1/0
df['was_subscription_paid'] = df['was_subscription_paid'].map({'Yes': 1, 'No': 0})

# Load into PostgreSQL
df.to_sql("subscriptions_staging", engine, if_exists="replace", index=False)

print("Data loaded into PostgreSQL successfully!")