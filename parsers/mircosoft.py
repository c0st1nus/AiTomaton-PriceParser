from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import re
import os
import time

def microsoft(url="https://azure.microsoft.com/en-us/pricing/details/phi-3/?cdn=disable"):
    start_time = time.time()
    geckodriver_path = os.getenv('GECKODRIVER_PATH', '/usr/local/bin/geckodriver')
    firefox_path = os.getenv('FIREFOX_PATH', '/usr/bin/firefox')
    # geckodriver_path = "C:\\geckodriver\\geckodriver.exe"
    # firefox_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    
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
    tables = soup.find_all('table', class_='data-table__table data-table__table--pricing')

    data = {}
    price_pattern = re.compile(r'\$([\d.]+)')

    for table in tables:
        for row in table.find('tbody').find_all('tr'):
            columns = row.find_all('td')
            model = columns[0].text.strip()
            
            input_price_match = price_pattern.search(columns[2].text.strip())
            output_price_match = price_pattern.search(columns[3].text.strip())
            
            if input_price_match and output_price_match:
                input_price = input_price_match.group(1)
                output_price = output_price_match.group(1)
                data[model] = {
                    "input_price": input_price,
                    "output_price": output_price
                }

    end_time = time.time()
    elapsed_time = end_time - start_time
    return data, elapsed_time

if __name__ == "__main__":
    result = microsoft()
    print(result)