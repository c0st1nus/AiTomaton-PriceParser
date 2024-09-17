import requests
import lxml.html
import json
import time

def replicate(url="https://replicate.com/pricing"):
    start_time = time.time()
    response = requests.get(url)
    html_content = response.content
    tree = lxml.html.fromstring(html_content)
    element = tree.xpath('/html/body/main/div/section[3]/div/script')
    if element:
        json_data = json.loads(element[0].text)
        models = json_data.get('officialModels', [])
        data = {}
        
        for model in models:
            full_name = model['full_name']
            input_price = model['cost_per_billing_unit_for_input_dollars']
            output_price = model['cost_per_billing_unit_for_output_dollars']
            data[full_name] = {
                "input_price": input_price,
                "output_price": output_price
            }
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        return data, elapsed_time
    else:
        return None, None
    
if __name__ == "__main__":
    result = replicate()
    print(result)