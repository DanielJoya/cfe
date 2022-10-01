#%% Get data from page
# Defaults imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Application imports
from selenium.webdriver.support.select import Select #Supports dropdown selection
from selenium.webdriver.common.by import By #Supports find_elements
import pandas as pd

# Local imports
from functions import GetDataFromSelect

# Initial request
options = Options()
options.add_experimental_option("detach", True) #Keep browser open after code is completed
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window() # Maximize window

driver.get("https://app.cfe.mx/Aplicaciones/CCFE/Tarifas/TarifasCRENegocio/Tarifas/PequenaDemandaBT.aspx")

prices = pd.DataFrame()

# Get months
select_element = driver.find_element(By.ID,'ContentPlaceHolder1_Fecha2_ddMes')
select_month = Select(select_element)
months = GetDataFromSelect(select_month)

# Get states
select_element = driver.find_element(By.ID,'ContentPlaceHolder1_EdoMpoDiv_ddEstado')
select_state = Select(select_element)
states = GetDataFromSelect(select_state)

for state in states:
    select_element = driver.find_element(By.ID,'ContentPlaceHolder1_EdoMpoDiv_ddEstado')
    select_state = Select(select_element)
    select_state.select_by_visible_text(state)

    # Get towns
    select_element = driver.find_element(By.ID,'ContentPlaceHolder1_EdoMpoDiv_ddMunicipio')
    select_town = Select(select_element)
    towns = GetDataFromSelect(select_town)

    for town in towns:
        select_element = driver.find_element(By.ID,'ContentPlaceHolder1_EdoMpoDiv_ddMunicipio')
        select_town = Select(select_element)
        select_town.select_by_visible_text(town)

        # Get divisions
        select_element = driver.find_element(By.ID,'ContentPlaceHolder1_EdoMpoDiv_ddDivision')
        select_division = Select(select_element)
        divisions = GetDataFromSelect(select_division)

        for division in divisions:
            select_element = driver.find_element(By.ID,'ContentPlaceHolder1_EdoMpoDiv_ddDivision')
            select_division = Select(select_element)
            select_division.select_by_visible_text(division)

            # Extract data
            divisionPrices = pd.DataFrame()
            for month in months:
                select_element = driver.find_element(By.ID,'ContentPlaceHolder1_Fecha2_ddMes')
                select_month = Select(select_element)
                select_month.select_by_visible_text(month)
                    
                table = pd.read_html(driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[2]/table[1]/tbody/tr[8]/td/table/tbody/tr[2]/td/table').get_attribute('outerHTML'))[0]
                
                if month == months[0]:
                    divisionPrices = table.iloc[:,:4]
                    divisionPrices['Estado'] = state
                    divisionPrices['Municipio'] = town
                    divisionPrices['Division'] = division

                divisionPrices[month] = table.iloc[:,-1]

            prices = pd.concat([prices, divisionPrices], ignore_index=True)

prices.to_csv("pdbt.csv")
