from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import re
import os

def novita(url="https://novita.ai/model-api/pricing"):
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
    data = {}
    price_pattern = re.compile(r'\$([\d.]+)')

    models = soup.find_all('div', class_='calcBoard_camp__GTRKG')
    for model in models:
        model_name = model.find('div', class_='calcBoard_title__V8DyI').text.strip()
        prices = model.find_all('span', class_='ant-tag-blue')
        input_price_match = price_pattern.search(prices[0].text.strip())
        output_price_match = price_pattern.search(prices[1].text.strip())

        if input_price_match and output_price_match:
            input_price = input_price_match.group(1)
            output_price = output_price_match.group(1)
            data[model_name] = {
                "input_price": input_price,
                "output_price": output_price
            }

    return data

if __name__ == "__main__":
    result = novita()
    print(result)