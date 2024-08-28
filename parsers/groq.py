from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import re

def groq(url="https://groq.com/enterprise-access/"):
    service = Service("C:\\geckodriver\\geckodriver.exe")
    options = webdriver.FirefoxOptions()
    options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    options.add_argument('--headless')
    driver = webdriver.Firefox(service=service, options=options)
    
    driver.get(url)
    driver.implicitly_wait(1)
    
    html_content = driver.page_source
    driver.quit()

    
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'id': 'tablepress-1'})
    data = {}

    for row in table.find('tbody').find_all('tr'):
        columns = row.find_all('td')
        model = columns[0].text.strip()
        input_price = re.search(r'\$([0-9.]+)', columns[2].text.strip()).group(1)
        output_price = re.search(r'\$([0-9.]+)', columns[3].text.strip()).group(1)
        
        data[model] = {
            "input_price": input_price,
            "output_price": output_price
        }
    
    return data

if __name__ == "__main__":
    result = groq()
    print(result)