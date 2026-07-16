CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE
);

CREATE TABLE weather (
    weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_date DATE NOT NULL UNIQUE,
    weather_condition TEXT NOT NULL,
    temperature REAL,
    precipitation REAL
);

CREATE TABLE events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    event_date DATE NOT NULL,
    day_of_week TEXT NOT NULL,
    start_time TEXT NOT NULL,
    venue_capacity INTEGER NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    is_holiday BOOLEAN NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

CREATE TABLE attendance_logs (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    weather_id INTEGER NOT NULL,
    attendance_count INTEGER NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (weather_id) REFERENCES weather(weather_id)
);