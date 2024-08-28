from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

def anthropic(url="https://www.anthropic.com/pricing#anthropic-api"):
    service = Service("C:\\geckodriver\\geckodriver.exe")
    options = webdriver.FirefoxOptions()
    options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    options.add_argument('--headless')
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(url)
    
    # Ожидание появления элемента с классом PricingCard_pricingCard__I0GPp
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'PricingCard_pricingCard__I0GPp'))
    )
    
    html_content = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html_content, 'html.parser')
    cards = soup.find_all('article', class_='PricingCard_pricingCard__I0GPp')

    data = {}
    price_pattern = re.compile(r'\$([\d.]+)')

    for card in cards:
        model = card.find('h3', class_='PricingCard_title__QrC94').text.strip()
        if model in ['Free', 'Pro', 'Team']:
            continue  # Пропускаем ненужные модели
        price_sections = card.find_all('div', class_='PricingCard_cost__m6Npy')
        price_data = {}
        for section in price_sections:
            caption = section.find('div', class_='text-caption').text.strip()
            if caption in ['Input', 'Output']:
                price_text = section.find('div', class_='PricingCard_price___wnbq').text.strip()
                match = price_pattern.search(price_text)
                if match:
                    price_data[caption] = match.group(1)  # Сохраняем цену как строку
        if price_data:  # Сохраняем только если есть нужные данные
            data[model] = price_data

    return data

# Пример вызова функции
if __name__ == '__main__':
    print(anthropic())