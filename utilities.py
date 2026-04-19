import requests
import json
import os
from datetime import datetime, timedelta


class WeatherForecast:
    def __init__(self, cache_file="weather_cache.json"):
        self.cache_file = cache_file
        self.data = self._load_cache()

    def _load_cache(self):
        """Internal method to load data from the file."""
        if not os.path.exists(self.cache_file):
            return {}
        with open(self.cache_file, 'r') as f:
            content = f.read()
            if not content:
                return {}
            return json.loads(content)

    def _save_cache(self):
        """Internal method to save data to the file."""
        with open(self.cache_file, 'w') as f:
            f.write(json.dumps(self.data, indent=4))

    def __setitem__(self, date, weather):
        """Allows: weather_forecast[date] = weather"""
        self.data[date] = weather
        self._save_cache()

    def __getitem__(self, date):
        """Allows: value = weather_forecast[date]"""
        # Logic: if in memory, return it; otherwise, call API
        if date in self.data:
            return self.data[date]

        # If not in cache, fetch from API
        print(f"Fetching data from API for {date}...")
        result = self._fetch_from_api(date)

        if result is not None and result >= 0:
            self[date] = result  # This triggers __setitem__
        return result

    def __iter__(self):
        """Allows: for date in weather_forecast:"""
        return iter(self.data.keys())

    def items(self):
        """Returns a generator of (date, weather) tuples."""
        for date, weather in self.data.items():
            yield (date, weather)

    def _fetch_from_api(self, date, lat=53.33, lon=-6.24):
        """Internal helper for API requests."""
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


def get_target_date():
    """Helper function (outside the class) for user input."""
    user_input = input("Enter a date (YYYY-mm-dd) or press Enter for tomorrow: ").strip()
    if not user_input:
        return (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    if len(user_input) == 10 and user_input[4] == '-' and user_input[7] == '-':
        return user_input
    return (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')