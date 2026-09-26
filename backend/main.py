from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from backend import models, schemas
from backend.database import engine, get_db
from backend.ml_service import predict_fare, get_dashboard_stats
from backend.ai_service import generate_driver_tip

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="NYC Taxi Fare & Revenue Advisor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "API running"}

@app.post("/predict", response_model=schemas.PredictResponse)
def predict(request: schemas.PredictRequest, db: Session = Depends(get_db)):
    if request.payment_type not in ["Card", "Cash"]:
        raise HTTPException(status_code=400, detail="payment_type must be 'Card' or 'Cash'")
    if request.trip_distance <= 0 or request.duration <= 0:
        raise HTTPException(status_code=400, detail="trip_distance and duration must be positive")

    predicted_fare = predict_fare(
        request.trip_distance, request.duration, request.passenger_count, request.payment_type
    )

    ai_tip = generate_driver_tip(
        request.trip_distance, request.duration, request.passenger_count,
        request.payment_type, predicted_fare
    )

    record = models.FarePrediction(
        trip_distance=request.trip_distance,
        duration=request.duration,
        passenger_count=request.passenger_count,
        payment_type=request.payment_type,
        predicted_fare=predicted_fare,
        ai_tip=ai_tip,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return schemas.PredictResponse(id=record.id, predicted_fare=predicted_fare, ai_tip=ai_tip)

@app.get("/history", response_model=list[schemas.HistoryItem])
def get_history(limit: int = 20, db: Session = Depends(get_db)):
    return db.query(models.FarePrediction).order_by(
        models.FarePrediction.created_at.desc()
    ).limit(limit).all()

@app.get("/dashboard-stats")
def dashboard_stats():
    return get_dashboard_stats()

@app.get("/usage-stats")
def usage_stats(db: Session = Depends(get_db)):
    total = db.query(models.FarePrediction).count()
    avg_fare = db.query(models.FarePrediction).with_entities(
        models.FarePrediction.predicted_fare
    ).all()
    avg = round(sum(f[0] for f in avg_fare) / len(avg_fare), 2) if avg_fare else 0
    return {"total_predictions_made": total, "avg_predicted_fare": avg}