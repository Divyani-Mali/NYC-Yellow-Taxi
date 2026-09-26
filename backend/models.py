from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from backend.database import Base

class FarePrediction(Base):
    __tablename__ = "fare_predictions"

    id = Column(Integer, primary_key=True, index=True)
    trip_distance = Column(Float, nullable=False)
    duration = Column(Float, nullable=False)
    passenger_count = Column(Integer, nullable=False)
    payment_type = Column(String, nullable=False)
    predicted_fare = Column(Float, nullable=False)
    ai_tip = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)