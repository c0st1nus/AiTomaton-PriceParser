import requests
from bs4 import BeautifulSoup
import time

def fireworks(url="https://fireworks.ai/pricing"):
    start_time = time.time()
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    
    tbody = soup.select_one('div.rounded:nth-child(6) > table:nth-child(1) > tbody:nth-child(2)')
    data = {
        "Any model 0-4B": {"input_price": None, "output_price": None},
        "Any model 4-16B": {"input_price": None, "output_price": None},
        "Any model 16B+": {"input_price": None, "output_price": None},
        "MoE 0-56B": {"input_price": None, "output_price": None},
        "MoE 56-176B": {"input_price": None, "output_price": None},
        "Yi Large": {"input_price": None, "output_price": None},
        "Meta Llama 3.1 405B": {"input_price": None, "output_price": None}
    }
    
    for row in tbody.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) < 2:
            continue
        model = columns[0].text.strip()
        price = columns[1].text.strip().replace('$', '')
        
        if "0B - 4B" in model:
            data["Any model 0-4B"]["input_price"] = price
            data["Any model 0-4B"]["output_price"] = price
        elif "4B - 16B" in model:
            data["Any model 4-16B"]["input_price"] = price
            data["Any model 4-16B"]["output_price"] = price
        elif "16.1B+" in model:
            data["Any model 16B+"]["input_price"] = price
            data["Any model 16B+"]["output_price"] = price
        elif "MoE 0B - 56B" in model:
            data["MoE 0-56B"]["input_price"] = price
            data["MoE 0-56B"]["output_price"] = price
        elif "MoE 56.1B - 176B" in model:
            data["MoE 56-176B"]["input_price"] = price
            data["MoE 56-176B"]["output_price"] = price
        elif "Yi Large" in model:
            data["Yi Large"]["input_price"] = price
            data["Yi Large"]["output_price"] = price
        elif "Meta Llama 3.1 405B" in model:
            data["Meta Llama 3.1 405B"]["input_price"] = price
            data["Meta Llama 3.1 405B"]["output_price"] = price
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    return data, elapsed_time

if __name__ == "__main__":
    result = fireworks()
    print(result)