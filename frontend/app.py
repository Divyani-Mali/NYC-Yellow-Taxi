import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="NYC Taxi Fare Advisor", page_icon="🚖", layout="wide")

# ---------------- Custom CSS ----------------
st.markdown("""
<style>
    .main { background-color: #f7f9fc; }
    .stButton>button {
        background-color: #f59e0b;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover { background-color: #d97706; }
    .card {
        background-color: white;
        color: #1e293b;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .fare-header {
        background: linear-gradient(90deg, #f59e0b, #fbbf24);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .fare-header h1 { color: white; margin: 0; font-size: 2.5rem; }
    .ai-box {
        background-color: #fffbeb;
        color: #1e293b;
        border-left: 4px solid #f59e0b;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        line-height: 1.6;
    }
    section[data-testid="stSidebar"] { background-color: #111827; }
    section[data-testid="stSidebar"] * { color: white !important; }
</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
st.sidebar.markdown("## 🚖 Taxi Fare Advisor")
st.sidebar.caption("ML + AI powered fare estimator")
st.sidebar.divider()
page = st.sidebar.radio("Navigate", ["💰 Fare Estimator", "📜 History", "📊 Dashboard"])

# ---------------- Fare Estimator ----------------
if page == "💰 Fare Estimator":
    st.markdown("<h1 style='text-align:center;'>NYC Taxi Fare Estimator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>Enter trip details for an AI-assisted fare estimate and driver tip</p>", unsafe_allow_html=True)
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        trip_distance = st.number_input("Trip Distance (miles)", min_value=0.1, max_value=50.0, value=3.0, step=0.1)
        duration = st.number_input("Trip Duration (minutes)", min_value=1.0, max_value=180.0, value=15.0, step=1.0)
    with col2:
        passenger_count = st.selectbox("Passenger Count", [1, 2, 3, 4, 5])
        payment_type = st.radio("Payment Type", ["Card", "Cash"], horizontal=True)

    if st.button("🔎 Estimate Fare", type="primary", use_container_width=True):
        with st.spinner("Calculating..."):
            try:
                response = requests.post(f"{API_URL}/predict", json={
                    "trip_distance": trip_distance,
                    "duration": duration,
                    "passenger_count": passenger_count,
                    "payment_type": payment_type
                })
            except requests.exceptions.ConnectionError:
                st.error("Backend not reachable. Make sure `uvicorn backend.main:app --reload` is running in a separate terminal.")
                st.stop()

        if response.status_code == 200:
            data = response.json()

            st.markdown(f"""
            <div class="fare-header">
                <p style="margin:0; opacity:0.9;">Estimated Fare</p>
                <h1>${data['predicted_fare']}</h1>
            </div>
            """, unsafe_allow_html=True)

            if data.get("ai_tip"):
                st.markdown(f"""
                <div class="ai-box">
                    <h3 style="margin-top:0;">🤖 Driver Tip</h3>
                    <p style="margin-bottom:0;">{data['ai_tip']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error(f"Prediction failed: {response.text}")

# ---------------- History ----------------
elif page == "📜 History":
    st.title("📜 Prediction History")
    try:
        history = requests.get(f"{API_URL}/history").json()
    except requests.exceptions.ConnectionError:
        st.error("Backend not reachable. Make sure `uvicorn backend.main:app --reload` is running.")
        st.stop()

    if not history:
        st.info("No predictions yet — try the Fare Estimator first.")
    else:
        for item in history:
            st.markdown(f"""
            <div class="card">
                <strong style="font-size:1.1rem;">${item['predicted_fare']} — {item['trip_distance']} mi, {item['duration']} min</strong><br>
                <span style="color:gray;">{item['passenger_count']} passenger(s), {item['payment_type']}</span><br>
                <span style="color:#9ca3af; font-size:0.85rem;">{item['created_at']}</span>
            </div>
            """, unsafe_allow_html=True)

# ---------------- Dashboard ----------------
elif page == "📊 Dashboard":
    st.title("📊 Historical Fare Analytics")

    stats = requests.get(f"{API_URL}/dashboard-stats").json()
    usage = requests.get(f"{API_URL}/usage-stats").json()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <p style="color:gray; margin-bottom:0.2rem;">Historical Trips Analyzed</p>
            <h2 style="color:#f59e0b; margin:0;">{stats['total_historical_trips']:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <p style="color:gray; margin-bottom:0.2rem;">Fare-Distance Correlation</p>
            <h2 style="color:#f59e0b; margin:0;">{stats['fare_distance_correlation']}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <p style="color:gray; margin-bottom:0.2rem;">Live Predictions Made</p>
            <h2 style="color:#f59e0b; margin:0;">{usage['total_predictions_made']}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Average Fare by Payment Type")
        st.bar_chart(stats["avg_fare_by_payment"])
    with col2:
        st.markdown("### Average Trip Distance by Payment Type")
        st.bar_chart(stats["avg_distance_by_payment"])

    st.write("")
    st.markdown("### Payment Type Split")
    st.bar_chart(stats["payment_type_split"])

    st.write("")
    st.markdown("### Fare Amount Distribution (Historical)")
    st.bar_chart(stats["fare_histogram"])