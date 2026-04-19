from utilities import WeatherForecast, get_target_date

def main():
    # 1. Create the object
    wf = WeatherForecast()

    # 2. Get target date
    target_date = get_target_date()

    # 3. Use __getitem__ syntax: it handles cache vs API internally!
    precipitation = wf[target_date]

    # 4. Display result
    if precipitation is None or precipitation < 0:
        print("I don't know.")
    elif precipitation > 0.0:
        print(f"It will rain. Precipitation: {precipitation} mm")
    else:
        print("It will not rain.")

    print("\n--- Summary of saved forecasts ---")
    # 5. Testing the items() generator
    for date, rain in wf.items():
        print(f"Date: {date} | Rain: {rain} mm")

    print("\n--- Iterating over saved dates ---")
    # 6. Testing the __iter__ method
    for saved_date in wf:
        print(f"Forecast known for: {saved_date}")

if __name__ == "__main__":
    main()