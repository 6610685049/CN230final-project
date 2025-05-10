import requests
import sqlite3


def main():
    data = fetch_weather_data()
    con = sqlite3.connect("tutorial.db")
    setup_database(con)
    save_data_to_db(con, data)
    run_analysis(con)
    con.close()


def fetch_weather_data():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 13.75,  # Bangkok
        "longitude": 100.5167,
        "hourly": "temperature_2m",
        "timezone": "Asia/Bangkok",
    }
    response = requests.get(url, params=params)
    return response.json()


def setup_database(con):
    cursor = con.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            temperature REAL
        )
    """
    )
    con.commit()


def save_data_to_db(con, weather_data):
    cursor = con.cursor()
    times = weather_data["hourly"]["time"]
    temperatures = weather_data["hourly"]["temperature_2m"]

    for t, temp in zip(times, temperatures):
        cursor.execute(
            "INSERT INTO weather (time, temperature) VALUES (?, ?)", (t, temp)
        )
    con.commit()


def run_analysis(con):
    cursor = con.cursor()

    print("\nค่าเฉลี่ยอุณหภูมิแยกตามวัน:")
    cursor.execute(
        """
        SELECT substr(time, 1, 10) as date, AVG(temperature) as avg_temp
        FROM weather
        GROUP BY date
        ORDER BY date
    """
    )
    for row in cursor.fetchall():
        print(f"วันที่: {row[0]} - ค่าเฉลี่ย: {row[1]:.2f}°C")

    print("\n5 ช่วงเวลาที่ร้อนที่สุด:")
    cursor.execute(
        """
        SELECT time, temperature
        FROM weather
        ORDER BY temperature DESC
        LIMIT 5
    """
    )
    for row in cursor.fetchall():
        print(f"{row[0]} - {row[1]:.2f}°C")


if __name__ == "__main__":
    main()
