import requests
from bs4 import BeautifulSoup

def cohere(url="https://cohere.com/pricing"):
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    model_selector = 'div.mx-auto:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2) > p:nth-child(1) > span:nth-child(1)'
    input_price_selector = 'div.mx-auto:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > p:nth-child(2)'
    output_price_selector = 'div.mx-auto:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > p:nth-child(2)'

    model_element = soup.select_one(model_selector)
    input_price_element = soup.select_one(input_price_selector)
    output_price_element = soup.select_one(output_price_selector)

    model = model_element.text.strip() if model_element else None
    input_price = input_price_element.text.strip().replace('$', '') if input_price_element else None
    output_price = output_price_element.text.strip().replace('$', '') if output_price_element else None

    data = {}
    if model:
        data[model] = {
            "input_price": input_price,
            "output_price": output_price
        }

    return data

if __name__ == "__main__":
    result = cohere()
    print(result)