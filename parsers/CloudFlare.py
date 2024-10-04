import requests
from bs4 import BeautifulSoup
import time

def cloudflare(url="https://developers.cloudflare.com/workers-ai/platform/pricing/"):
    start_time = time.time()
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Используем указанный XPath для нахождения таблицы
    table = soup.select_one('body > div > div > div > div > main > div:nth-of-type(2) > div > div:nth-of-type(1) > table:nth-of-type(1)')
    
    data = {
        "Any model 0-3B": {"input_price": None, "output_price": None},
        "Any model 3-8B": {"input_price": None, "output_price": None},
        "Any model 8-20B": {"input_price": None, "output_price": None},
        "Any model 20-40B": {"input_price": None, "output_price": None},
        "Any model 40B+": {"input_price": None, "output_price": None}
    }
    
    for row in table.find('tbody').find_all('tr'):
        columns = row.find_all('td')
        model = columns[0].text.strip()
        price = columns[1].text.strip().split(' ')[0].replace('$', '')
        
        if "<= 3B" in model:
            data["Any model 0-3B"]["input_price"] = price
            data["Any model 0-3B"]["output_price"] = price
        elif "3.1B - 8B" in model:
            data["Any model 3-8B"]["input_price"] = price
            data["Any model 3-8B"]["output_price"] = price
        elif "8.1B - 20B" in model:
            data["Any model 8-20B"]["input_price"] = price
            data["Any model 8-20B"]["output_price"] = price
        elif "20.1B - 40B" in model:
            data["Any model 20-40B"]["input_price"] = price
            data["Any model 20-40B"]["output_price"] = price
        elif "40.1B+" in model:
            data["Any model 40B+"]["input_price"] = price
            data["Any model 40B+"]["output_price"] = price
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    return data, elapsed_time

if __name__ == "__main__":
    result = cloudflare()
    print(result)