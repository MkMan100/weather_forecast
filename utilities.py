import requests
import json
import os
from datetime import datetime, timedelta

CACHE_FILE = "weather_cache.json"


def get_target_date():
    user_input = input("Enter a date (YYYY-mm-dd) or press Enter for tomorrow: ").strip()

    if not user_input:
        return (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    if len(user_input) == 10 and user_input[4] == '-' and user_input[7] == '-':
        return user_input

    print("Invalid format detected. Using tomorrow's date as fallback.")
    return (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')


def load_cache():
    # Check if file exists
    if not os.path.exists(CACHE_FILE):
        return {}

    with open(CACHE_FILE, 'r') as f:
        content = f.read()
        if not content:
            return {}
        return json.loads(content)


def save_cache(cache_data):
    with open(CACHE_FILE, 'w') as f:
        f.write(json.dumps(cache_data, indent=4))


def fetch_weather_from_api(date, lat=53.33, lon=-6.24):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={date}&end_date={date}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        daily = data.get('daily')

        if daily:
            precip_list = daily.get('precipitation_sum')
            if precip_list and len(precip_list) > 0:
                return precip_list[0]

    return -1