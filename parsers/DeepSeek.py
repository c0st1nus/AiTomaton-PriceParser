from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import re
import os

def deepseek(url="https://platform.deepseek.com/api-docs/pricing/"):
    geckodriver_path = os.getenv('GECKODRIVER_PATH', '/usr/local/bin/geckodriver')
    firefox_path = os.getenv('FIREFOX_PATH', '/usr/bin/firefox')

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
    
    table = soup.find('table')
    
    data = {}
    
    for row in table.find('tbody').find_all('tr'):
        columns = row.find_all('td')
        model = re.sub(r'\s*\(1\)', '', columns[0].text.strip())
        input_price_cache_miss = re.search(r'\$([0-9.]+)', columns[4].text.strip()).group(1)
        output_price = re.search(r'\$([0-9.]+)', columns[5].text.strip()).group(1)
        
        data[model] = {
            "input_price": input_price_cache_miss,
            "output_price": output_price
        }
    
    return data

if __name__ == "__main__":
    result = deepseek()
    print(result)