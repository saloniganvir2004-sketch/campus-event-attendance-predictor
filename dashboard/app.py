import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Campus Event Attendance Predictor",
    layout="wide"
)

DB_PATH = Path("database/database.db")

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
conn.close()