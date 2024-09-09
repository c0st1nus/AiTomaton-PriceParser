import requests
from bs4 import BeautifulSoup
import time

def cloudflare(url="https://developers.cloudflare.com/workers-ai/platform/pricing/"):
    start_time = time.time()
    response = requests.get(url)
    response.raise_for_status()  # Проверка на успешный запрос
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find_all('table')[5]  # Изменено на find_all для выбора 6-й таблицы
    
    data = {}
    
    for row in table.find('tbody').find_all('tr'):
        columns = row.find_all('td')
        model = columns[0].text.strip()
        input_price = columns[1].text.strip().replace('$', '')
        output_price = columns[2].text.strip().replace('$', '')
        
        data[model] = {
            "input_price": input_price,
            "output_price": output_price
        }
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    return data, elapsed_time

if __name__ == "__main__":
    result = cloudflare()
    print(result)