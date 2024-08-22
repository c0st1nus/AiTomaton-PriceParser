# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

def mistral(url = "https://mistral.ai/technology/"):
    # Получение HTML-кода страницы
    response = requests.get(url)
    html_content = response.text

    # Парсинг HTML-кода с помощью BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Поиск всех таблиц с классом 'price-table'
    tables = soup.find_all('table', class_='price-table')

    # Инициализация словаря для хранения данных
    data = {}

    # Регулярное выражение для извлечения числовой части цены
    price_pattern = re.compile(r'\$([\d.]+)')

    # Извлечение данных из каждой таблицы
    for table in tables:
        for row in table.find('tbody').find_all('tr'):
            columns = row.find_all('td')
            model = columns[0].text.strip()
            
            input_price_match = price_pattern.search(columns[3].text.strip())
            output_price_match = price_pattern.search(columns[4].text.strip())
            
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
    result = mistral()
    print(result)