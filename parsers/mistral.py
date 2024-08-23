import requests
from bs4 import BeautifulSoup
import re

def mistral(url = "https://mistral.ai/technology/"):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table', class_='price-table')
    data = {}
    price_pattern = re.compile(r'\$([\d.]+)')

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

if __name__ == "__main__":
    result = mistral()
    print(result)