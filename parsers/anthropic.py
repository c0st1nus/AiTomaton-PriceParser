from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import os

def anthropic(url="https://www.anthropic.com/pricing#anthropic-api"):
    geckodriver_path = os.getenv('GECKODRIVER_PATH', '/usr/local/bin/geckodriver')
    firefox_path = os.getenv('FIREFOX_PATH', '/usr/bin/firefox')

    service = Service(geckodriver_path)
    options = webdriver.FirefoxOptions()
    options.binary_location = firefox_path
    options.add_argument('--headless')
    driver = webdriver.Firefox(service=service, options=options)
    
    driver.get(url)
    driver.implicitly_wait(1)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'PricingCard_pricingCard__I0GPp'))
    )
    
    html_content = driver.page_source
    driver.quit()
    with open('anthropic.html', 'w', encoding='utf-8') as file:
        file.write(html_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    cards = soup.find_all('article', class_='PricingCard_pricingCard__I0GPp')

    data = {}
    price_pattern = re.compile(r'\$([\d.]+)')

    for card in cards:
        title_element = card.find('h3')
        if title_element is None:
            continue
        model = title_element.text.strip()
        if model in ['Free', 'Pro', 'Team']:
            continue
        price_sections = card.find_all('div', class_='PricingCard_cost__m6Npy')
        price_data = {"input_price": None, "output_price": None}  # Изменено
        for section in price_sections:
            caption = section.find('div', class_='text-caption').text.strip()
            if caption == 'Input':
                price_text = section.find('div', class_='PricingCard_price___wnbq').text.strip()
                match = price_pattern.search(price_text)
                if match:
                    price_data["input_price"] = match.group(1)  # Изменено
            elif caption == 'Output':  # Изменено
                price_text = section.find('div', class_='PricingCard_price___wnbq').text.strip()
                match = price_pattern.search(price_text)
                if match:
                    price_data["output_price"] = match.group(1)  # Изменено
        if price_data["input_price"] or price_data["output_price"]:  # Изменено
            data[model] = price_data

    return data

if __name__ == '__main__':
    print(anthropic())