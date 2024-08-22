import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

def openAI(url="https://openai.com/api/pricing/"):
    # Настройка Selenium с использованием geckodriver
    options = Options()
    options.headless = True
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    
    # Переход на страницу
    driver.get(url)
    driver.implicitly_wait(10)  # Ждем 10 секунд для загрузки страницы

    # Получение HTML-кода страницы
    html_content = driver.page_source
    driver.quit()

    # Парсинг HTML-кода с помощью BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Поиск всех элементов с классом 'grid col-span-full grid-cols-autofit'
    grids = soup.find_all('div', class_='grid col-span-full grid-cols-autofit')

    # Инициализация словаря для хранения данных
    data = {}

    # Регулярное выражение для извлечения числовой части цены
    price_pattern = re.compile(r'\$([\d.]+)')

    # Извлечение данных из каждого элемента
    for grid in grids:
        columns = grid.find_all('div', class_='m:border-l-[1px] border-gray-20 text-small flex flex-col gap-y-6xs m:flex-row m:py-4xs m:px-3xs px-5xs py-2xs')
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

# Пример вызова функции
if __name__ == "__main__":
    result = openAI()
    print(result)