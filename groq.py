# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'
}

def groq(url="https://wow.groq.com/"):
    # Получение HTML-кода страницы
    response = requests.get(url, headers=headers)
    html_content = response.text

    # Парсинг HTML-кода с помощью BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Поиск таблицы с классом 'pmatrix'
    table = soup.find('table', class_='pmatrix')

    # Проверка, что таблица найдена
    if table is None:
        return {}

    # Инициализация словаря для хранения данных
    data = {}

    # Регулярное выражение для извлечения числовой части цены
    price_pattern = re.compile(r'\$([\d.]+)')

    # Извлечение данных из таблицы
    for row in table.find('tbody').find_all('tr'):
        columns = row.find_all('td')
        model = columns[0].text.strip()
        speed = columns[1].text.strip()
        
        price_text = columns[2].text.strip()
        prices = price_pattern.findall(price_text)
        
        if len(prices) == 2:
            input_price, output_price = prices
        else:
            input_price = prices[0]
            output_price = None
        
        data[model] = {
            "input_price": input_price,
            "output_price": output_price
        }

    return data

# Пример вызова функции
if __name__ == "__main__":
    result = groq()
    print(result)