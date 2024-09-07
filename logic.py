import json
from datetime import datetime
from parsers import *
import os
import handler

def get_data():
    service = ''
    result = {}
    print("Start of parsing")
    print('=' * 20)
    service = 'openrouter'
    result['openrouter'] = openrouter()
    service = 'groq'
    result['groq'] = groq()
    log_success(service)
    service = 'mistral'
    result['mistral'] = mistral()
    log_success(service)
    service = 'cohere'
    result['cohere'] = cohere()
    log_success(service)
    service = 'openAI'
    result['openAI'] = openAI()
    log_success(service)
    service = 'anthropic'
    result['anthropic'] = anthropic()
    log_success(service)
    service = 'google'
    result['google'] = google()
    log_success(service)
    service = 'microsoft'
    result['microsoft'] = microsoft()
    log_success(service)
    service = 'deepseek'
    result['deepseek'] = deepseek()
    log_success(service)
    service = 'cloudflare'
    result['cloudflare'] = cloudflare()
    log_success(service)
    service = 'novita'
    result['novita'] = cloudflare()
    log_success(service)
    print('Parsing Success')
    print('=' * 20)
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    with open("log.txt", "a") as log_file:
        log_file.write(f"{current_time} [Success] Parsing Success\n")
    data = result
    consolidated_data = {}
    for provider, models in data.items():
        for model_name, prices in models.items():
            if not model_name or 'input_price' not in prices or 'output_price' not in prices:
                continue
            try:
                input_price = round(float(prices['input_price'].replace(',', '.')), 2)
                output_price = round(float(prices['output_price'].replace(',', '.')), 2)
            except ValueError:
                continue
            if input_price < 0 or input_price >= 40 or output_price <= 0 or output_price >= 40:
                continue
            prices['input_price'] = input_price
            prices['output_price'] = output_price
            found = False
            for existing_name in consolidated_data.keys():
                if similarity(existing_name, model_name):
                    consolidated_data[existing_name][provider] = prices
                    found = True
                    break
            if not found:
                consolidated_data[model_name] = {provider: prices}
    handler.save_data(consolidated_data, calculate_average_prices(consolidated_data))

def log_success(service):
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    log_message = f"{current_time} [Success] The {service} has been parsed\n"
    with open("log.txt", "a") as log_file:
        log_file.write(log_message)

def similarity(s1, s2):
    s1, s2 = ''.join(filter(str.isalnum, s1.lower())), ''.join(filter(str.isalnum, s2.lower()))
    intersection = len(set(s1) & set(s2))
    similarity_ratio = intersection / max(len(s1), len(s2))
    return similarity_ratio >= 1

def calculate_average_prices(data):
    total_input_price = 0
    total_output_price = 0
    input_count = 0
    output_count = 0

    for model, providers in data.items():
        for provider, prices in providers.items():
            if 'input_price' in prices:
                try:
                    total_input_price += float(str(prices['input_price']).replace(',', '.'))
                    input_count += 1
                except ValueError:
                    pass
            if 'output_price' in prices:
                try:
                    total_output_price += float(str(prices['output_price']).replace(',', '.'))
                    output_count += 1
                except ValueError:
                    pass

    av_input_price = total_input_price / input_count if input_count > 0 else 0
    av_output_price = total_output_price / output_count if output_count > 0 else 0
    average_prices = {
        "av_input_price": av_input_price,
        "av_output_price": av_output_price
    }
    return average_prices