"""
One-time script: downloads the full NYC taxi dataset, cleans it using the
same logic as the original notebook, saves a 100k-row sample locally, and
trains + saves the fare prediction model.

Run this once:  python scripts/prepare_and_train.py
"""
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print("Downloading dataset (this may take a few minutes, ~6.4M rows)...")
df = pd.read_csv("https://query.data.world/s/3thg6ofefyce2qejr4ukpqcvceddjc?dws=00000")
print(f"Downloaded: {df.shape[0]} rows")

# Same cleaning steps as the original notebook
df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
df['duration'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60

df = df[['passenger_count', 'payment_type', 'fare_amount', 'trip_distance', 'duration']]
df.dropna(inplace=True)

df['passenger_count'] = df['passenger_count'].astype('int64')
df['payment_type'] = df['payment_type'].astype('int64')
df.drop_duplicates(inplace=True)

df = df[df['payment_type'] < 3]
df = df[(df['passenger_count'] > 0) & (df['passenger_count'] < 6)]
df['payment_type'] = df['payment_type'].replace([1, 2], ['Card', 'Cash'])

df = df[df['fare_amount'] > 0]
df = df[df['trip_distance'] > 0]
df = df[df['duration'] > 0]

# Remove outliers (IQR method, same as notebook)
for col in ['fare_amount', 'trip_distance', 'duration']:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

print(f"After cleaning: {df.shape[0]} rows")

# Take a 100k sample for the app (still statistically solid, loads fast)
sample_size = min(100_000, len(df))
df_sample = df.sample(n=sample_size, random_state=42).reset_index(drop=True)

sample_path = os.path.join(BASE_DIR, "data", "taxi_data_clean.csv")
df_sample.to_csv(sample_path, index=False)
print(f"Saved cleaned sample ({sample_size} rows) to {sample_path}")

# Train the model on the full cleaned data (not just the sample) for best accuracy
df_encoded = pd.get_dummies(df, columns=['payment_type'], drop_first=False)

X = df_encoded[['trip_distance', 'duration', 'passenger_count', 'payment_type_Card']]
y = df_encoded['fare_amount']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\nModel Performance:")
print("MAE:", mean_absolute_error(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))
print("R² Score:", r2_score(y_test, y_pred))

model_path = os.path.join(BASE_DIR, "ml_models", "fare_model.pkl")
with open(model_path, "wb") as f:
    pickle.dump(model, f)
print(f"\nModel saved to {model_path}")