import requests
from bs4 import BeautifulSoup
import re
import time

def fireworks(url="https://fireworks.ai/pricing"):
    start_time = time.time()
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='table--outline')
    data = {}
    price_pattern = re.compile(r'\$([\d.]+)')
    required_models = [
        "DBRX", "Mixtral 8x22B", "Mixtral 8x7B", 
        "Meta Llama 3.1 405B", "Yi Large"
    ]

    if table:
        for row in table.find('tbody').find_all('tr'):
            columns = row.find_all('td')
            model = columns[0].text.strip()
            price_match = price_pattern.search(columns[1].text.strip())
            
            if price_match:
                price = price_match.group(1)
                for required_model in required_models:
                    if required_model in model:
                        clean_model = required_model
                        data[clean_model] = {
                            "input_price": price,
                            "output_price": price
                        }

    end_time = time.time()
    elapsed_time = end_time - start_time
    return data, elapsed_time

if __name__ == "__main__":
    print(fireworks())