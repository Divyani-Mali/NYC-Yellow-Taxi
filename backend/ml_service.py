import pickle
import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = pickle.load(open(os.path.join(BASE_DIR, "ml_models", "fare_model.pkl"), "rb"))
taxi_data = pd.read_csv(os.path.join(BASE_DIR, "data", "taxi_data_clean.csv"))


def predict_fare(trip_distance, duration, passenger_count, payment_type):
    payment_type_card = 1 if payment_type.lower() == "card" else 0

    input_df = pd.DataFrame([{
        "trip_distance": trip_distance,
        "duration": duration,
        "passenger_count": passenger_count,
        "payment_type_Card": payment_type_card
    }])

    predicted = model.predict(input_df)[0]
    return round(float(predicted), 2)


def get_dashboard_stats():
    """Historical stats computed from the cleaned dataset, for the dashboard charts."""
    avg_fare_by_payment = taxi_data.groupby("payment_type")["fare_amount"].mean().to_dict()
    avg_distance_by_payment = taxi_data.groupby("payment_type")["trip_distance"].mean().to_dict()
    payment_type_split = taxi_data["payment_type"].value_counts(normalize=True).mul(100).round(1).to_dict()

    fare_distance_corr = float(taxi_data["fare_amount"].corr(taxi_data["trip_distance"]))

    fare_bins = pd.cut(taxi_data["fare_amount"], bins=10).value_counts().sort_index()
    fare_histogram = {
        f"${interval.left:.0f}-{interval.right:.0f}": int(count)
        for interval, count in fare_bins.items()
    }
    
    return {
        "avg_fare_by_payment": avg_fare_by_payment,
        "avg_distance_by_payment": avg_distance_by_payment,
        "payment_type_split": payment_type_split,
        "fare_distance_correlation": round(fare_distance_corr, 3),
        "fare_histogram": fare_histogram,
        "total_historical_trips": len(taxi_data),
    }