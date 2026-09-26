from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_predict_valid_input():
    response = client.post("/predict", json={
        "trip_distance": 3.5,
        "duration": 15,
        "passenger_count": 1,
        "payment_type": "Card"
    })
    assert response.status_code == 200
    data = response.json()
    assert "predicted_fare" in data
    assert data["predicted_fare"] > 0

def test_predict_invalid_payment_type():
    response = client.post("/predict", json={
        "trip_distance": 3.5,
        "duration": 15,
        "passenger_count": 1,
        "payment_type": "Bitcoin"
    })
    assert response.status_code == 400

def test_predict_negative_distance():
    response = client.post("/predict", json={
        "trip_distance": -1,
        "duration": 15,
        "passenger_count": 1,
        "payment_type": "Cash"
    })
    assert response.status_code == 400

def test_history_after_prediction():
    client.post("/predict", json={
        "trip_distance": 2.0, "duration": 10,
        "passenger_count": 2, "payment_type": "Cash"
    })
    response = client.get("/history")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_dashboard_stats():
    response = client.get("/dashboard-stats")
    assert response.status_code == 200
    data = response.json()
    assert "avg_fare_by_payment" in data
    assert "fare_distance_correlation" in data

def test_usage_stats():
    response = client.get("/usage-stats")
    assert response.status_code == 200
    assert "total_predictions_made" in response.json()