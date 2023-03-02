# Third party libraries
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # Supports find_elements
from selenium.webdriver.support.select import Select  # Supports dropdown selection
from webdriver_manager.chrome import ChromeDriverManager

# Local imports
from .crawler_utils import GetDataFromSelect, select_option


def get_prices(link, tariff, ids):

    file_name = tariff + ".csv"

    driver = driver_initialization(link)

    years = GetDataFromSelect(driver, ids["year"])

    months = GetDataFromSelect(driver, ids["month"], 0)
    months.pop(-1)  # Always remove the last month since there is no data available

    states = GetDataFromSelect(driver, ids["state"], 0)

    prices, lastState, lastMonth, lastMonthIndex, lastStateIndex = data_initialization(
        file_name, months, states
    )  # Initialize data

    if not (((lastState == states[-1]) & (lastMonth == months[-1]))):

        for month in months[lastMonthIndex:]:

            select_option(driver, ids["month"], month)

            for state in states[lastStateIndex + 1 :]:

                select_option(driver, ids["state"], state)

                towns = GetDataFromSelect(driver, ids["town"], 0)

                for town in towns:
                    select_option(driver, ids["town"], town)

                    # Get divisions
                    divisions = GetDataFromSelect(driver, ids["division"], 0)

                    for division in divisions:
                        select_option(driver, ids["division"], division)
                        prices = extract_data(
                            driver, ids, months, month, state, town, division, prices
                        )

                prices.to_csv(file_name, index=False)
            lastStateIndex = -1


def driver_initialization(link):
    # Initial request
    options = Options()
    options.add_experimental_option(
        "detach", True
    )  # Keep browser open after code is completed
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.maximize_window()  # Maximize window

    driver.get(link)

    return driver


def data_initialization(file_name, months, states):
    try:
        prices = pd.read_csv(file_name)
        lastMonth = prices.columns[-1]
        lastMonthIndex = months.index(lastMonth)
        lastMonthData = prices[prices[lastMonth].notnull()]
        lastState = lastMonthData["Estado"].iloc[-1]
        lastStateIndex = states.index(lastState)

    except:
        prices = pd.DataFrame()
        lastMonth = months[0]
        lastMonthIndex = 0
        lastState = states[0]
        lastStateIndex = -1

    if lastState == states[-1]:
        lastMonthIndex = lastMonthIndex + 1
        lastStateIndex = -1

    return prices, lastState, lastMonth, lastMonthIndex, lastStateIndex


def extract_data(driver, ids, months, month, state, town, division, prices):
    divisionPrices = pd.DataFrame()

    table = pd.read_html(
        driver.find_element(
            By.XPATH,
            ids["table"],
        ).get_attribute("outerHTML")
    )[0]

    if month == months[0]:

        divisionPrices = table.iloc[:, :4]
        divisionPrices["Estado"] = state
        divisionPrices["Municipio"] = town
        divisionPrices["Division"] = division
        divisionPrices[month] = table.iloc[:, -1]

        prices = pd.concat([prices, divisionPrices], axis=0, ignore_index=True)
    else:
        divisionPrices[month] = table.iloc[:, -1]
        fixedPrice = divisionPrices.loc[0, month]
        variablePrice = divisionPrices.loc[1, month]

        prices.loc[
            (prices["Estado"] == state)
            & (prices["Municipio"] == town)
            & (prices["Division"] == division)
            & (prices["Cargo"] == "Fijo"),
            month,
        ] = fixedPrice
        prices.loc[
            (prices["Estado"] == state)
            & (prices["Municipio"] == town)
            & (prices["Division"] == division)
            & (prices["Cargo"] == "Variable (Energía)"),
            month,
        ] = variablePrice

    return prices
