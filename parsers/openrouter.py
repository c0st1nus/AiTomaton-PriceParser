import requests
import json
import time

def openrouter(url="https://openrouter.ai/api/v1/models"):
    start_time = time.time()
    result = requests.get(url).content.decode('utf-8')
    data = json.loads(result)["data"]
    
    result = {}

    for i in range(0, len(data)):
        result[data[i]["name"]] = {
            "input_price": str(float(data[i]["pricing"]["prompt"]) * 1000000),
            "output_price": str(float(data[i]["pricing"]["completion"]) * 1000000)
        }
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time

if __name__ == "__main__":
    result = openrouter()
    with open('openrouter.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False, indent=4))