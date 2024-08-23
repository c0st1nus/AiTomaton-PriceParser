import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'
}

def groq(url="https://wow.groq.com/"):
    response = requests.get(url, headers=headers)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    table = soup.find('table', class_='pmatrix')

    if table is None:
        return {}

    data = {}

    price_pattern = re.compile(r'\$([\d.]+)')

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

if __name__ == "__main__":
    result = groq()
    print(result)