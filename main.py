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

# Select states
select_element = driver.find_element(By.ID,'ContentPlaceHolder1_EdoMpoDiv_ddEstado')
select_states = Select(select_element)
states = GetDataFromSelect(select_states)
select_states.select_by_index(1) # Select the first state

# Select towns
select_element = driver.find_element(By.ID,'ContentPlaceHolder1_EdoMpoDiv_ddMunicipio')
select_towns = Select(select_element)
towns = GetDataFromSelect(select_towns)
select_towns.select_by_index(1) # Select the first town

# Select divisions
select_element = driver.find_element(By.ID,'ContentPlaceHolder1_EdoMpoDiv_ddDivision')
select_divisions = Select(select_element)
divisions = GetDataFromSelect(select_divisions)
select_divisions.select_by_index(1) # Select the first division

# Select month
select_element = driver.find_element(By.ID,'ContentPlaceHolder1_Fecha2_ddMes')
select_month = Select(select_element)
months = GetDataFromSelect(select_month)

# Get tariff name, description, type of charge and units
select_month.select_by_visible_text(months[0]) # Select the first month
table = pd.read_html(driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[2]/table[1]/tbody/tr[8]/td/table/tbody/tr[2]/td/table').get_attribute('outerHTML'))[0]
tariffData = table[table.columns[:-1]]

#%% Extract data
prices = pd.DataFrame()

for month in months:
    select_element = driver.find_element(By.ID,'ContentPlaceHolder1_Fecha2_ddMes')
    select_month = Select(select_element)
    select_month.select_by_visible_text(month) # Select the first month
    table = pd.read_html(driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[2]/table[1]/tbody/tr[8]/td/table/tbody/tr[2]/td/table').get_attribute('outerHTML'))[0]
    prices[month] = table.iloc[:,-1]

#%% Manipulate data


