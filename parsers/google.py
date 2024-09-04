import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import os

def transform_data(data):
    new_data = {}
    for key, value in data.items():
        new_key = key.replace(" СѓР¶Рµ РґРѕСЃС‚СѓРїРµРЅ", "")
        new_value = {
            'input_price': value['input_price'].replace('$', '').split()[0],
            'output_price': value['output_price'].replace('$', '').split()[0]
        }
        new_data[new_key] = new_value
    return new_data

def google(url="https://ai.google.dev/pricing?hl=ru"):
    geckodriver_path = os.getenv('GECKODRIVER_PATH', '/usr/local/bin/geckodriver')
    firefox_path = os.getenv('FIREFOX_PATH', '/usr/bin/firefox')

    # Использование путей в коде
    service = Service(geckodriver_path)
    options = webdriver.FirefoxOptions()
    options.binary_location = firefox_path
    options.add_argument('--headless')
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(url)
    driver.implicitly_wait(1)
    html_content = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html_content, 'html.parser')
    model_selector = r'#gemini-1\.5-flash-available-now'
    input_price_selector = r'.gemini-pricing-tabs > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > p:nth-child(1)'
    output_price_selector = r'.gemini-pricing-tabs > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > p:nth-child(1)'
    model_element = soup.select_one(model_selector)
    input_price_element = soup.select_one(input_price_selector)
    output_price_element = soup.select_one(output_price_selector)
    model = model_element.text.strip() if model_element else None
    input_price = input_price_element.text.strip() if input_price_element else None
    output_price = output_price_element.text.strip() if output_price_element else None
    data = {}
    if model:
        data[model] = {
            "input_price": input_price,
            "output_price": output_price
        }
    data = transform_data(data)
    return data

if __name__ == "__main__":
    result = google()
    print(result)