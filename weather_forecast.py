from utilities import WeatherForecast, get_target_date

def main():
    # Create the object
    wf = WeatherForecast()

    target_date = get_target_date()

    precipitation = wf[target_date]

    # Display result
    if precipitation is None or precipitation < 0:
        print("I don't know.")
    elif precipitation > 0.0:
        print(f"It will rain. Precipitation: {precipitation} mm")
    else:
        print("It will not rain.")

    print("\n--- Summary of saved forecasts ---")
    
    for date, rain in wf.items():
        print(f"Date: {date} | Rain: {rain} mm")

    print("\n--- Iterating over saved dates ---")
    
    for saved_date in wf:
        print(f"Forecast known for: {saved_date}")

if __name__ == "__main__":
    main()
