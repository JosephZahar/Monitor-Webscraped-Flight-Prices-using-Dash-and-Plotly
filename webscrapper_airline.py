import pandas as pd
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def webscrape_airlines():
    # open csv
    webscrapped_flights = pd.read_csv("/Users/macbookpro/PycharmProjects/Airline Webscrapper/webscrapped_flights.csv")
    today_date = date.today()
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # navigate to UA website
    # departure flights
    for day in range(12, 19):
        driver.get(
            f"https://www.united.com/en/us/fsr/choose-flights?f=LHR&t=IAD&d=2023-03-{day}&tt=1&sc=7&px=1&taxng=1&newHP=True&clm=7&st=bestmatches&tqp=R"
        )

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="flightResults-content"]/div[3]/div[1]/div/div[2]/div[1]/div[1]/div/button',
                )
            )
        )

        price = driver.find_element(
            By.CLASS_NAME,
            "app-components-Shopping-PriceCard-styles__priceValue--21Ki_",
        ).text.strip()[1:]
        webscrapped_flights = webscrapped_flights.append(
            {
                "airline_name": "United Airlines",
                "type": "Departure",
                "flight_date": f"{day} March",
                "timestamp": today_date,
                "price": price,
            },
            ignore_index=True,
        )

    # return flights
    for day in range(13, 20):
        driver.get(
            f"https://www.united.com/en/us/fsr/choose-flights?f=IAD&t=LHR&d=2023-04-{day}&tt=1&sc=7&px=1&taxng=1&newHP=True&clm=7&st=bestmatches&tqp=R"
        )

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="flightResults-content"]/div[3]/div[1]/div/div[2]/div[1]/div[1]/div/button',
                )
            )
        )

        price = driver.find_element(
            By.CLASS_NAME,
            "app-components-Shopping-PriceCard-styles__priceValue--21Ki_",
        ).text.strip()[1:]
        webscrapped_flights = webscrapped_flights.append(
            {
                "airline_name": "United Airlines",
                "type": "Return",
                "flight_date": f"{day} April",
                "timestamp": today_date,
                "price": price,
            },
            ignore_index=True,
        )

    # Calculate Total Flight Price for every date combination
    departure_df = webscrapped_flights[
        (webscrapped_flights.type == "Departure") & (webscrapped_flights.timestamp == today_date)
    ]
    return_df = webscrapped_flights[
        (webscrapped_flights.type == "Return") & (webscrapped_flights.timestamp == today_date)
    ]

    for _, row_dep in departure_df.iterrows():
        for _, row_ret in return_df.iterrows():
            webscrapped_flights = webscrapped_flights.append(
                {
                    "airline_name": "United Airlines",
                    "type": "Total",
                    "flight_date": f"{row_dep.flight_date} – {row_ret.flight_date}",
                    "timestamp": today_date,
                    "price": int(row_dep.price.replace(",", "")) + int(row_ret.price.replace(",", "")),
                },
                ignore_index=True,
            )

    webscrapped_flights.to_csv("webscrapped_flights.csv")


webscrape_airlines()


