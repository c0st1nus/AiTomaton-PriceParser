from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def openrouter(url="https://openrouter.ai/docs/models"):
    # Настройка Selenium WebDriver
    service = Service("C:\\geckodriver\\geckodriver.exe")  # Укажите путь к geckodriver
    options = webdriver.FirefoxOptions()
    options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"  # Укажите путь к Firefox
    options.add_argument('--headless')  # Запуск в фоновом режиме
    driver = webdriver.Firefox(service=service, options=options)

    try:
        # Открытие страницы
        driver.get(url)

        # Ожидание элемента
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.w-full"))
        )
        # Получение содержимого страницы
        html_content = driver.page_source
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return {}
    finally:
        driver.quit()

    # Парсинг HTML-кода с помощью BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Поиск всех строк таблицы с классом 'text-sm'
    rows = soup.find_all('tr', class_='text-sm')

    # Инициализация словаря для хранения данных
    data = {}

    # Регулярное выражение для извлечения числовой части цены
    price_pattern = re.compile(r'\$([\d.]+)')

    # Извлечение данных из каждой строки
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

# Пример вызова функции
if __name__ == "__main__":
    result = openrouter()
    print(result)