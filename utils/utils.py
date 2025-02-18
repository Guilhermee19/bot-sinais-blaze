from selenium.webdriver.common.by import By

# Tenta extrair as informações
def getInfo(driver, search, return_element=False):
    try:
        element = driver.find_element(By.XPATH, search)
        if return_element:
            return element
        return element.text
    except:
        return '--' if not return_element else None
