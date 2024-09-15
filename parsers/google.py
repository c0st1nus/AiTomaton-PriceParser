import time
import re
from bs4 import BeautifulSoup
import requests

def gemini1(gemini_pro_tab):
    if gemini_pro_tab:
        model_name_elem = gemini_pro_tab.find('h2', class_='gemini-tier-name')
        if model_name_elem:
            model_name = model_name_elem.get('data-text', '').strip()
            model_name = model_name.replace("Available now", "").strip()
        
        input_price = None
        output_price = None
        
        tier_subgroups = gemini_pro_tab.find_all('div', class_='gemini-tier-group')
        for subgroup in tier_subgroups:
            for line in subgroup.find_all('div', class_='gemini-tier-line'):
                label = line.find('p', class_='gemini-type-l2')
                value = line.find('p', class_='gemini-type-t3')
                if label and value:
                    label_text = label.text.strip().lower()
                    value_text = value.text.strip()
                    price_match = re.search(r'\$([0-9.]+)', value_text)
                    if price_match:
                        price = price_match.group(1)
                        if 'input pricing' in label_text:
                            input_price = price
                        elif 'output pricing' in label_text:
                            output_price = price
                    elif 'free of charge' in value_text.lower():
                        if 'input pricing' in label_text:
                            input_price = 'Free of charge'
                        elif 'output pricing' in label_text:
                            output_price = 'Free of charge'
        
        if model_name and input_price and output_price:
            return {"input_price": input_price, "output_price": output_price}

def google(url="https://ai.google.dev/pricing/"):
    start_time = time.time()
    result = requests.get(url).content
    soup = BeautifulSoup(result, 'html.parser')
    
    models = {}
    tabs = soup.find_all('div', class_='gemini-pricing-tabs gemini-tabs-data')
    
    for tab in tabs:
        pricing_tabs = tab.find_all('div', class_='gemini-pricing-tab', recursive=True)
        
        for pricing_tab in pricing_tabs:
            model_name_elem = pricing_tab.find('h2', class_='gemini-tier-name')
            if model_name_elem:
                model_name = model_name_elem.get('data-text', '').strip()
                model_name = model_name.replace("Available now", "").strip()
            else:
                continue
            
            input_price = None
            output_price = None
            
            tier_subgroups = pricing_tab.find_all('div', class_='gemini-tier-subgroup', recursive=True)
            for subgroup in tier_subgroups:
                for line in subgroup.find_all('div', class_='gemini-tier-line', recursive=True):
                    label = line.find('p', class_='gemini-type-l2')
                    value = line.find('p', class_='gemini-type-t3')
                    if label and value:
                        label_text = label.text.strip().lower()
                        value_text = value.text.strip()
                        price_match = re.search(r'\$([0-9.]+)', value_text)
                        if price_match:
                            price = price_match.group(1)
                            if 'input pricing' in label_text:
                                input_price = price
                            elif 'output pricing' in label_text:
                                output_price = price
            
            if model_name and input_price and output_price:
                models[model_name] = {
                    'input_price': input_price,
                    'output_price': output_price
                }
    models["Gemini 1 Pro"] = gemini1(soup.find('div', {'data-tab': 'gemini-1-pro'}))

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    return models, elapsed_time

if __name__ == "__main__":
    print(google())