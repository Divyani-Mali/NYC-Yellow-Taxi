import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def generate_driver_tip(trip_distance, duration, passenger_count, payment_type, predicted_fare):
    if client is None:
        print("AI tip skipped: GEMINI_API_KEY not found in environment.")
        return None

    prompt = f"""
You are a helpful assistant for taxi drivers analyzing a fare estimate.

Trip distance: {trip_distance} miles
Trip duration: {duration} minutes
Passenger count: {passenger_count}
Payment type: {payment_type}
Predicted fare: ${predicted_fare}

Known patterns from historical NYC taxi data:
- Card payments tend to have slightly higher average fares than cash
- Short trips (under 2 miles) sometimes have unexpectedly high fares due to base charges
- Trip distance is the strongest driver of fare amount

Write a short (3-4 sentence), practical tip for the driver about this specific trip —
whether the fare looks typical for the distance/duration, and one general
suggestion for maximizing earnings based on the patterns above. Keep it
conversational, no headings.
"""

    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )
            return response.text.strip()
        except Exception as e:
            print(f"AI tip attempt {attempt + 1} failed: {e}")
            if attempt < max_retries:
                time.sleep(2)
            else:
                return None