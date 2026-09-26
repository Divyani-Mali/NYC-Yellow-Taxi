from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PredictRequest(BaseModel):
    trip_distance: float
    duration: float
    passenger_count: int
    payment_type: str   # "Card" or "Cash"

class PredictResponse(BaseModel):
    id: int
    predicted_fare: float
    ai_tip: Optional[str] = None

class HistoryItem(BaseModel):
    id: int
    trip_distance: float
    duration: float
    passenger_count: int
    payment_type: str
    predicted_fare: float
    created_at: datetime

    class Config:
        from_attributes = True