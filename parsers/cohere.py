import requests
from bs4 import BeautifulSoup

def mistral(url="https://cohere.com/pricing"):
    # Получение HTML-кода страницы
    response = requests.get(url)
    html_content = response.content

    # Парсинг HTML-кода с помощью BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # CSS селекторы для извлечения данных
    model_selector = 'div.mx-auto:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2) > p:nth-child(1) > span:nth-child(1)'
    input_price_selector = 'div.mx-auto:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > p:nth-child(2)'
    output_price_selector = 'div.mx-auto:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > p:nth-child(2)'

    # Извлечение данных с проверкой на наличие элементов
    model_element = soup.select_one(model_selector)
    input_price_element = soup.select_one(input_price_selector)
    output_price_element = soup.select_one(output_price_selector)

    model = model_element.text.strip() if model_element else None
    input_price = input_price_element.text.strip() if input_price_element else None
    output_price = output_price_element.text.strip() if output_price_element else None

    # Формирование словаря с данными
    data = {}
    if model:
        data[model] = {
        "input_price": input_price,
        "output_price": output_price
    }

    return data

# Пример вызова функции
if __name__ == "__main__":
    result = mistral()
    print(result)