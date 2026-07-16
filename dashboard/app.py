import joblib
import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Campus Event Attendance Predictor",
    layout="wide"
)

DB_PATH = Path("database/database.db")
MODEL_PATH = Path("data/models/linear_regression.pkl")
model = joblib.load(MODEL_PATH)

conn = sqlite3.connect(DB_PATH)

events = pd.read_sql("""
SELECT
e.event_name,
c.category_name,
e.event_date,
e.day_of_week,
e.start_time,
e.venue_capacity,
w.weather_condition,
a.attendance_count
FROM events e
JOIN categories c
ON e.category_id = c.category_id
JOIN attendance_logs a
ON e.event_id = a.event_id
JOIN weather w
ON a.weather_id = w.weather_id
""", conn)

st.title("🎓 Campus Event Attendance Predictor")

st.sidebar.header("Filters")

category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(events["category_name"].unique().tolist())
)

weather = st.sidebar.selectbox(
    "Weather",
    ["All"] + sorted(events["weather_condition"].unique().tolist())
)

filtered = events.copy()

if category != "All":
    filtered = filtered[filtered["category_name"] == category]

if weather != "All":
    filtered = filtered[filtered["weather_condition"] == weather]

st.subheader("Historical Events")

st.dataframe(filtered, width="stretch")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Events", len(filtered))

with col2:
    st.metric(
        "Average Attendance",
        round(filtered["attendance_count"].mean(), 2) if len(filtered) else 0
    )

with col3:
    st.metric(
        "Maximum Attendance",
        filtered["attendance_count"].max() if len(filtered) else 0
    )

st.subheader("Attendance by Category")

category_chart = (
    filtered.groupby("category_name")["attendance_count"]
    .mean()
    .reset_index()
)

st.bar_chart(
    category_chart,
    x="category_name",
    y="attendance_count"
)

st.subheader("Attendance by Weather")

weather_chart = (
    filtered.groupby("weather_condition")["attendance_count"]
    .mean()
    .reset_index()
)

st.bar_chart(
    weather_chart,
    x="weather_condition",
    y="attendance_count"
)

st.subheader("Attendance Distribution")

line_chart = (
    filtered.set_index("event_name")[["attendance_count"]]
)

st.line_chart(line_chart)

st.divider()

st.header("Predict Attendance")

venue_capacity = st.number_input(
    "Venue Capacity",
    min_value=10,
    max_value=5000,
    value=200
)

is_weekend = st.selectbox(
    "Weekend",
    [0, 1]
)

is_holiday = st.selectbox(
    "Holiday",
    [0, 1]
)

month = st.slider(
    "Month",
    1,
    12,
    7
)

day = st.slider(
    "Day",
    1,
    31,
    15
)

start_hour = st.slider(
    "Start Hour",
    0,
    23,
    10
)

if st.button("Predict Attendance"):
    feature_names = [
        "venue_capacity",
        "is_weekend",
        "is_holiday",
        "month",
        "day",
        "start_hour"
    ]

    model_input = pd.DataFrame([[ 
        venue_capacity,
        is_weekend,
        is_holiday,
        month,
        day,
        start_hour
    ]], columns=feature_names)

    prediction = model.predict(model_input)[0]

    st.success(f"Predicted Attendance: {prediction:.0f}")
conn.close()