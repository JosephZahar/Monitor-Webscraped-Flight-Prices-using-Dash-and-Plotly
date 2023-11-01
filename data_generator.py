import csv
import random
from datetime import datetime, timedelta


def generate_data():
    airline_name = "United Airlines"
    departure_dates = [f"{i} March" for i in range(12, 19)]
    return_dates = [f"{i} April" for i in range(13, 20)]
    base_departure_price = [1880, 1850, 1200, 1000, 1900, 1990, 1760]
    return_prices = [643, 731, 916, 694, 732, 493, 493]
    timestamp_start = datetime.strptime("2023-01-29", "%Y-%m-%d")
    timestamp_end = datetime.strptime("2023-06-29", "%Y-%m-%d")

    data = []

    current_timestamp = timestamp_start
    while current_timestamp <= timestamp_end:
        # Departure data
        for i, date in enumerate(base_departure_price):
            price = base_departure_price[i] + random.randint(-500, 500)  # Fluctuation
            data.append([airline_name, "Departure", date, current_timestamp.strftime("%Y-%m-%d"), f"{price:,}"])

        # Return data
        for i, date in enumerate(return_dates):
            price = return_prices[i] + random.randint(-200, 100)  # Fluctuation
            data.append([airline_name, "Return", date, current_timestamp.strftime("%Y-%m-%d"), f"{price:,}"])

        # Total data
        for dep_date in departure_dates:
            for i, ret_date in enumerate(return_dates):
                total_price = base_departure_price[i] + sum(
                    return_prices[:return_dates.index(ret_date) + 1]) + random.randint(-100, 100)  # Fluctuation
                data.append([airline_name, "Total", f"{dep_date} – {ret_date}", current_timestamp.strftime("%Y-%m-%d"),
                             f"{total_price:,}"])

        current_timestamp += timedelta(days=1)

    return data


# Generate the data
data = generate_data()

# Save the data to a CSV file
with open('src/data/flight_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["airline_name", "type", "flight_date", "timestamp", "price"])  # Header row
    for row in data:
        writer.writerow(row)