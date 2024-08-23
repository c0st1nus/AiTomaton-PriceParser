import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

def anthropic(url="https://www.anthropic.com/pricing#anthropic-api"):
    service = Service("C:\\geckodriver\\geckodriver.exe")
    options = webdriver.FirefoxOptions()
    options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    options.add_argument('--headless')
    driver = webdriver.Firefox(service=service, options=options)

    driver.get("https://www.anthropic.com/pricing#anthropic-api")
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, 'html.parser')

    cards = soup.find_all('article', class_='PricingCard_pricingCard__I0GPp PricingCard_rows__aON_s')

    data = {}

    price_pattern = re.compile(r'\$([\d.]+)')

    for card in cards:
        model = card.find('h3', class_='PricingCard_title__QrC94').text.strip()
        prices = card.find_all('div', class_='PricingCard_price___wnbq')

        input_price = price_pattern.search(prices[0].text.strip()).group(1) if prices else None
        output_price = price_pattern.search(prices[-1].text.strip()).group(1) if prices else None

        if input_price and output_price:
            data[model] = {
                "input_price": input_price,
                "output_price": output_price
            }

    return data

if __name__ == "__main__":
    result = anthropic()
    print(result)