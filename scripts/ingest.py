import pandas as pd
import os

# Paths
RAW_PATH = "/home/eng-linda/Downloads/mavenflix-data-platform/Streaming+Video+Subscriptions/Subscription Cohort Analysis Data.csv"
STAGING_PATH = "data/staging/cleaned_subscriptions.csv"

def load_data():
    df = pd.read_csv(RAW_PATH)
    print("Raw data loaded:")
    print(df.head())
    return df

def basic_cleaning(df):
    # Convert dates
    df['created_date'] = pd.to_datetime(df['created_date'])
    df['canceled_date'] = pd.to_datetime(df['canceled_date'])

    # Handle missing canceled_date (active subscriptions)
    df['is_active'] = df['canceled_date'].isna()

    # Subscription length
    df['subscription_length_days'] = (
        df['canceled_date'] - df['created_date']
    ).dt.days

    # Fill active subscriptions with today's date
    df['subscription_length_days'] = df['subscription_length_days'].fillna(0)

    return df

def save_to_staging(df):
    os.makedirs("data/staging", exist_ok=True)
    df.to_csv(STAGING_PATH, index=False)
    print(f"Cleaned data saved to {STAGING_PATH}")

if __name__ == "__main__":
    df = load_data()
    df = basic_cleaning(df)
    save_to_staging(df)