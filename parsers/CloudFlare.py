from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os

def cloudflare(url="https://developers.cloudflare.com/workers-ai/platform/pricing/"):
    geckodriver_path = os.getenv('GECKODRIVER_PATH', '/usr/local/bin/geckodriver')
    firefox_path = os.getenv('FIREFOX_PATH', '/usr/bin/firefox')

    service = Service(geckodriver_path)
    options = webdriver.FirefoxOptions()
    options.binary_location = firefox_path
    options.add_argument('--headless')
    driver = webdriver.Firefox(service=service, options=options)
    
    driver.get(url)
    driver.implicitly_wait(1)
    
    table_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[2]/div/div[1]/table[6]')
    html_content = table_element.get_attribute('outerHTML')
    driver.quit()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    table = soup.find('table')
    
    data = {}
    
    for row in table.find('tbody').find_all('tr'):
        columns = row.find_all('td')
        model = columns[0].text.strip()
        input_price = columns[1].text.strip().replace('$', '')
        output_price = columns[2].text.strip().replace('$', '')
        
        data[model] = {
            "input_price": input_price,
            "output_price": output_price
        }
    
    return data 

if __name__ == "__main__":
    result = cloudflare()
    print(result)