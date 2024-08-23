from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def openrouter(url="https://openrouter.ai/docs/models"):
    service = Service("C:\\geckodriver\\geckodriver.exe")
    options = webdriver.FirefoxOptions()
    options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    options.add_argument('--headless')
    driver = webdriver.Firefox(service=service, options=options)

    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.w-full"))
        )
        html_content = driver.page_source
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {}
    finally:
        driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')
    rows = soup.find_all('tr', class_='text-sm')
    data = {}
    price_pattern = re.compile(r'\$([\d.]+)')

    for row in rows:
        columns = row.find_all('td')
        if len(columns) >= 5:
            model = columns[0].text.strip()
            input_price_match = price_pattern.search(columns[1].text.strip())
            output_price_match = price_pattern.search(columns[2].text.strip())
            
            if input_price_match and output_price_match:
                input_price = input_price_match.group(1)
                output_price = output_price_match.group(1)
                data[model] = {
                    "input_price": input_price,
                    "output_price": output_price
                }

    return data

if __name__ == "__main__":
    result = openrouter()
    print(result)