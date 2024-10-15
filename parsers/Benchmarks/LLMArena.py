import re
import os
import json
import threading
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException

def load_config():
    with open("config.json", "r") as config_file:
        return json.load(config_file)

def setup_driver(config):
    geckodriver_path = os.getenv('GECKODRIVER_PATH', config['driver'])
    firefox_path = os.getenv('FIREFOX_PATH', config['browser'])
    service = Service(geckodriver_path)
    options = Options()
    options.binary_location = firefox_path
    options.add_argument('--headless')
    return webdriver.Firefox(service=service, options=options)

def fetch_element_content(driver, element_xpath):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, element_xpath)))
    except UnexpectedAlertPresentException:
        alert = driver.switch_to.alert
        alert.dismiss()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, element_xpath)))
    element = driver.find_element(By.XPATH, element_xpath)
    return element.get_attribute('outerHTML')

def process_json_content(element_content):
    json_content = element_content.replace('<script>window.gradio_config = ', '').replace(';</script>', '')
    try:
        return json.loads(json_content)["components"][140]["props"]["value"]["data"]
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Ошибка при обработке JSON: {e}")
        return None

def extract_data(json_data, result, pattern):
    for i in json_data:
        matches = pattern.findall(i[1])
        if matches:
            result[matches[0]] = i[2]

def LLMArena():
    start_time = time.time()
    config = load_config()
    driver = setup_driver(config)
    driver.get('https://lmarena.ai/')
    
    element_xpath = '/html/head/script[2]'
    element_content = fetch_element_content(driver, element_xpath)
    driver.quit()
    
    if not element_content:
        print("Не удалось получить содержимое элемента.")
        return {}, 0
    
    json_data = process_json_content(element_content)
    
    if not json_data:
        print("Не удалось обработать JSON-содержимое.")
        return {}, 0
    
    result = {}
    pattern = re.compile(r'">(.*?)</a>')
    
    extract_thread = threading.Thread(target=extract_data, args=(json_data, result, pattern))
    extract_thread.start()
    extract_thread.join()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time

if __name__ == "__main__":
    print(LLMArena())