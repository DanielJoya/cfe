#%% Get data from page
# Defaults imports
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # Supports find_elements

# Application imports
from selenium.webdriver.support.select import Select  # Supports dropdown selection
from webdriver_manager.chrome import ChromeDriverManager

# Local imports
from functions import GetDataFromSelect

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

driver.get(
    "https://app.cfe.mx/Aplicaciones/CCFE/Tarifas/TarifasCRENegocio/Tarifas/PequenaDemandaBT.aspx"
)

# Get months
select_element = driver.find_element(By.ID, "ContentPlaceHolder1_Fecha2_ddMes")
select_month = Select(select_element)
months = GetDataFromSelect(select_month)

# Reading saved data
try:
    prices = pd.read_csv("pdbt.csv")
    lastMonth = prices.columns[-1]
    lastMonthIndex = months.index(lastMonth)

except:
    prices = pd.DataFrame()
    lastMonthIndex = 0

# Scrape only if the last month has not been extracted

for month in months[lastMonthIndex:]:
    # Get states
    select_element = driver.find_element(
        By.ID, "ContentPlaceHolder1_EdoMpoDiv_ddEstado"
    )
    select_state = Select(select_element)
    states = GetDataFromSelect(select_state)

    lastState = prices["Estado"].iloc[-1]
    lastStateIndex = states.index(lastState)

    #% Select month
    select_element = driver.find_element(By.ID, "ContentPlaceHolder1_Fecha2_ddMes")
    select_month = Select(select_element)
    select_month.select_by_visible_text(month)

    monthPrices = pd.DataFrame()

    if lastState != states[-1]:

        for state in states[lastStateIndex + 1 :]:
            select_element = driver.find_element(
                By.ID, "ContentPlaceHolder1_EdoMpoDiv_ddEstado"
            )
            select_state = Select(select_element)
            select_state.select_by_visible_text(state)

            # Get towns
            select_element = driver.find_element(
                By.ID, "ContentPlaceHolder1_EdoMpoDiv_ddMunicipio"
            )
            select_town = Select(select_element)
            towns = GetDataFromSelect(select_town)

            for town in towns:
                select_element = driver.find_element(
                    By.ID, "ContentPlaceHolder1_EdoMpoDiv_ddMunicipio"
                )
                select_town = Select(select_element)
                select_town.select_by_visible_text(town)

                # Get divisions
                select_element = driver.find_element(
                    By.ID, "ContentPlaceHolder1_EdoMpoDiv_ddDivision"
                )
                select_division = Select(select_element)
                divisions = GetDataFromSelect(select_division)

                for division in divisions:
                    select_element = driver.find_element(
                        By.ID, "ContentPlaceHolder1_EdoMpoDiv_ddDivision"
                    )
                    select_division = Select(select_element)
                    select_division.select_by_visible_text(division)

                    # Extract data
                    divisionPrices = pd.DataFrame()

                    table = pd.read_html(
                        driver.find_element(
                            By.XPATH,
                            '//*[@id="content"]/div/div[1]/div[2]/table[1]/tbody/tr[8]/td/table/tbody/tr[2]/td/table',
                        ).get_attribute("outerHTML")
                    )[0]

                    divisionPrices[month] = table.iloc[:, -1]

                    if month == months[0]:

                        divisionPrices = table.iloc[:, :4]
                        divisionPrices["Estado"] = state
                        divisionPrices["Municipio"] = town
                        divisionPrices["Division"] = division

                        prices = pd.concat(
                            [prices, divisionPrices], axis=0, ignore_index=True
                        )

                    else:
                        fixedPrice = divisionPrices.loc[0, month]
                        variablePrice = divisionPrices.loc[1, month]
                        prices.loc[
                            (prices["Estado"] == state)
                            & (prices["Municipio"] == town)
                            & (prices["Division"] == division)
                            & (prices["Cargo"] == "fijo"),
                            month,
                        ] = fixedPrice
                        prices.loc[
                            (prices["Estado"] == state)
                            & (prices["Municipio"] == town)
                            & (prices["Division"] == division)
                            & (prices["Cargo"] == "Variable (Energía)"),
                            month,
                        ] = variablePrice
            prices.to_csv("pdbt.csv", index=False)

# %%
