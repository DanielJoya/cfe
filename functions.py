from selenium.webdriver.support.select import Select #Supports dropdown selection

def GetDataFromSelect(select_object):
    DataList = []
    all_available_options = select_object.options

    for option in all_available_options:
        DataList.append(option.text)
    
    DataList.pop(0)

    return DataList