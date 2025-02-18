from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Tenta extrair as informações
def getInfo(driver, search, return_element=False):
    try:
        element = driver.find_element(By.XPATH, search)
        if return_element:
            return element
        return element.text
    except:
        return '--' if not return_element else None

def startChromeProd():
    # Configurações do navegador
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--headless")  # Ativa o modo headless

    # Define o caminho do ChromeDriver
    chrome_driver_path = "/usr/bin/chromedriver"

    # Inicializa o ChromeDriver corretamente
    service = Service(chrome_driver_path)
    nav = webdriver.Chrome(service=service)
    return nav

def startChromeDev():
    # Configurações do navegador
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--headless")  # Ativa o modo headless

    # Inicializar navegador
    nav = webdriver.Chrome(options=chrome_options)
    return nav