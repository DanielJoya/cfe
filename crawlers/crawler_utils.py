from selenium.webdriver.common.by import By  # Supports find_elements
from selenium.webdriver.support.select import Select  # Supports dropdown selection


def GetDataFromSelect(driver, identifier, rem=None):
    DataList = []
    select_element = driver.find_element(By.ID, identifier)
    select_object = Select(select_element)
    all_available_options = select_object.options

    for option in all_available_options:
        DataList.append(option.text)

    if rem != None:
        DataList.pop(rem)

    return DataList


def select_option(driver, identifier, element):
    select_element = driver.find_element(By.ID, identifier)
    select_object = Select(select_element)
    select_object.select_by_visible_text(element)
