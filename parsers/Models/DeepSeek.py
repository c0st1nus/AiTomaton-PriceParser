from bs4 import BeautifulSoup
import re
import time
import requests

def deepseek(url="https://api-docs.deepseek.com/quick_start/pricing"):
    start_time = time.time()
    response = requests.get(url)
    html_content = response.content
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    table = soup.find('table')
    
    data = {}
    
    for row in table.find('tbody').find_all('tr'):
        columns = row.find_all('td')
        model = re.sub(r'\s*\(1\)', '', columns[0].text.strip())
        input_price_cache_miss = re.search(r'\$([0-9.]+)', columns[4].text.strip()).group(1)
        output_price = re.search(r'\$([0-9.]+)', columns[5].text.strip()).group(1)
        
        data[model] = {
            "input_price": input_price_cache_miss,
            "output_price": output_price
        }
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    return data, elapsed_time

if __name__ == "__main__":
    result = deepseek()
    print(result)