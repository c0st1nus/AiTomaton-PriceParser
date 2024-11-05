import requests
import time
import json

def novita(url="https://novita.ai/api/chat-models"):
    start_time = time.time()
    result = requests.get(url)
    result.raise_for_status()
    json_data = result.json()
    data = {}
    
    for model_data in json_data["data"]:
        model = model_data['title'].split('/')[-1]
        input_price = str(model_data['input_token_price_per_m'] / 10000)
        output_price = str(model_data['output_token_price_per_m'] / 10000)
        
        data[model] = {
            "input_price": input_price,
            "output_price": output_price
        }
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    return data, elapsed_time

if __name__ == "__main__":
    result = novita()
    print(result)