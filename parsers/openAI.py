import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import os

def openAI(url="https://openai.com/api/pricing/"):
    geckodriver_path = os.getenv('GECKODRIVER_PATH', '/usr/local/bin/geckodriver')
    firefox_path = os.getenv('FIREFOX_PATH', '/usr/bin/firefox')

    # Использование путей в коде
    service = Service(geckodriver_path)
    options = webdriver.FirefoxOptions()
    options.binary_location = firefox_path
    options.add_argument('--headless')
    driver = webdriver.Firefox(service=service, options=options)
    
    driver.get(url)
    driver.implicitly_wait(10)

    html_content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')
    grid = soup.find('div', class_='w-full grid m:inline-block transition-all duration-300 grid-rows-[0fr]')
    
    data = {}
    price_pattern = re.compile(r'\$([\d.]+)')

    if grid:
        rows = grid.find_all('div', class_='grid col-span-full grid-cols-autofit')
        for row in rows:
            columns = row.find_all('div', class_='m:border-l-[1px] border-gray-20 text-small flex flex-col gap-y-6xs m:flex-row m:py-4xs m:px-3xs px-5xs py-2xs')
            if len(columns) == 3:
                model = columns[0].find('span').text.strip() if columns[0].find('span') else ''
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
    result = openAI()
    print(result)