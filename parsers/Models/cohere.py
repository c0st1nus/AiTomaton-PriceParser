import requests
from bs4 import BeautifulSoup
import time

def cohere(url="https://cohere.com/pricing"):
    start_time = time.time()
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    models = soup.select('div[data-component="ModelCard"]')
    data = {}

    for model_element in models:
        model_name = model_element.select_one('p.text-3xl').text.strip() if model_element.select_one('p.text-3xl') else None
        
        input_price = model_element.select_one('div:nth-of-type(1) p.text-2xl').text.strip().replace('$', '') if model_element.select_one('div:nth-of-type(1) p.text-2xl') else None
        output_price = model_element.select_one('div:nth-of-type(2) p.text-2xl').text.strip().replace('$', '') if model_element.select_one('div:nth-of-type(2) p.text-2xl') else None

        if model_name:
            data[model_name] = {
                "input_price": input_price,
                "output_price": output_price
            }

    end_time = time.time()
    elapsed_time = end_time - start_time
    return data, elapsed_time

if __name__ == "__main__":
    result = cohere()
    print(result)