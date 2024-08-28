from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def openrouter(url="https://openrouter.ai/docs/models"):
    service = Service("C:\\geckodriver\\geckodriver.exe")
    options = webdriver.FirefoxOptions()
    options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    options.add_argument('--headless')
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(url)
    
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.w-full.table-fixed'))
        )
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table.w-full.table-fixed tbody tr'))
        )
    except Exception as e:
        driver.quit()
        return {"error": f"Table not found: {str(e)}"}
    
    html_content = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='w-full table-fixed')
    
    if table is None:
        return {"error": "Table not found"}
    
    tbody = table.find('tbody', class_='divide-y')
    rows = tbody.find_all('tr', class_='text-sm')

    data = {}
    for row in rows:
        title = row.get('title')
        columns = row.find_all('td')
        model_name = columns[0].find('a').text.strip()
        
        input_div = columns[1].find('div')
        input_price = input_div.contents[0].strip().replace('$', '') if input_div else 'N/A'
        
        output_div = columns[2].find('div')
        output_price = output_div.contents[0].strip().replace('$', '') if output_div else 'N/A'
        
        data[model_name] = {
            "input_price": input_price,
            "output_price": output_price
        }
    return data

if __name__ == "__main__":
    result = openrouter()
    print(result)