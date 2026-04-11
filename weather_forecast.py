import utilities


def main():
    target_date = utilities.get_target_date()

    # Load existing results from file
    cache = utilities.load_cache()

    if target_date in cache:
        print(f"Result found in cache for {target_date}:")
        precipitation = cache[target_date]
    else:
        print(f"Fetching data from API for {target_date}...")
        precipitation = utilities.fetch_weather_from_api(target_date)

        # Save if result is valid
        if precipitation is not None and precipitation >= 0:
            cache[target_date] = precipitation
            utilities.save_cache(cache)

    # results
    if precipitation is None or precipitation < 0:
        print("I don't know.")
    elif precipitation > 0.0:
        print(f"It will rain. Precipitation: {precipitation} mm")
    else:
        print("It will not rain.")


if __name__ == "__main__":
    main()