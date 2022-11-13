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
from extractMonth import extract_month

# Initial request
options = Options()
options.add_experimental_option("detach", True) #Keep browser open after code is completed
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window() # Maximize window

driver.get("https://app.cfe.mx/Aplicaciones/CCFE/Tarifas/TarifasCRENegocio/Tarifas/PequenaDemandaBT.aspx")

# Get months
select_element = driver.find_element(By.ID,'ContentPlaceHolder1_Fecha2_ddMes')
select_month = Select(select_element)
months = GetDataFromSelect(select_month)

#Reading saved data
try:
    prices = pd.read_csv('pdbt.csv')
    lastMonth = prices.columns[-1]
    lastMonthIndex = months.index(lastMonth)

except:
    prices = pd.DataFrame() 
    lastMonthIndex = 0

# Scrape only if the last month has not been extracted
if lastMonthIndex < len(months) - 1:
    for month in months[lastMonthIndex+1:]:
        prices = extract_month(month)

