import json
from datetime import datetime
from parsers import *

def get_data():
    service = ''
    try:
        result = {}
        print("Start of parsing")
        print('=' * 20)

        service = 'openrouter'
        print("Parsing the openrouter source")
        print('=' * 20)
        result['openrouter'] = openrouter()
        log_success(service)

        service = 'groq'
        print("Parsing the groq source")
        print('=' * 20)
        result['groq'] = groq()
        log_success(service)

        service = 'mistral'
        print("Parsing the mistral source")
        print('=' * 20)
        result['mistral'] = mistral()
        log_success(service)

        service = 'cohere'
        print("Parsing the cohere source")
        print('=' * 20)
        result['cohere'] = cohere()
        log_success(service)

        service = 'openAI'
        print("Parsing the openAI source")
        print('=' * 20)
        result['openAI'] = openAI()
        log_success(service)

        service = 'anthropic'
        print("Parsing the anthropic source")
        print('=' * 20)
        result['anthropic'] = anthropic()
        log_success(service)

        service = 'google'
        print("Parsing the google source")
        print('=' * 20)
        result['google'] = google()
        log_success(service)

        service = 'microsoft'
        print("Parsing the microsoft source")
        print('=' * 20)
        result['microsoft'] = microsoft()
        log_success(service)

        service = 'deepseek'
        print("Parsing the deepseek source")
        print('=' * 20)
        result['deepseek'] = deepseek()
        log_success(service)

        service = 'cloudflare'
        print("Parsing the cloudflare source")
        print('=' * 20)
        result['cloudflare'] = cloudflare()
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
                found = False
                for existing_name in consolidated_data.keys():
                    if similarity(existing_name, model_name):
                        consolidated_data[existing_name][provider] = prices
                        found = True
                        break
                if not found:
                    consolidated_data[model_name] = {provider: prices}
        current_date = datetime.now().strftime("%d-%m-%Y")
        with open(f"prices/{current_date}.json", 'w', encoding='utf-8') as f:
            json.dump(consolidated_data, f, indent=4, ensure_ascii=False)
        calculate_average_prices(consolidated_data)
    except Exception as e:
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
        log_message = f"{current_time} [Error] An error occurred while parsing {service}: {str(e)}\n"
        print('=' * 20)
        print("An error occurred while parsing, check the log.txt")
        print('=' * 20)
        with open("log.txt", "a") as log_file:
            log_file.write(log_message)

def log_success(service):
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    log_message = f"{current_time} [Success] The {service} has been parsed\n"
    with open("log.txt", "a") as log_file:
        log_file.write(log_message)

def similarity(s1, s2):
    s1, s2 = ''.join(filter(str.isalnum, s1.lower())), ''.join(filter(str.isalnum, s2.lower()))
    intersection = len(set(s1) & set(s2))
    similarity_ratio = intersection / max(len(s1), len(s2))
    return similarity_ratio >= 0.45

def calculate_average_prices(data):
    total_input_price = 0
    total_output_price = 0
    input_count = 0
    output_count = 0

    for model, providers in data.items():
        for provider, prices in providers.items():
            if 'input_price' in prices:
                try:
                    total_input_price += float(prices['input_price'].replace(',', '.'))
                    input_count += 1
                except ValueError:
                    pass
            if 'output_price' in prices:
                try:
                    total_output_price += float(prices['output_price'].replace(',', '.'))
                    output_count += 1
                except ValueError:
                    pass

    av_input_price = total_input_price / input_count if input_count > 0 else 0
    av_output_price = total_output_price / output_count if output_count > 0 else 0

    current_date = datetime.now().strftime("%d.%m.%Y")
    average_prices = {
        "av_input_price": av_input_price,
        "av_output_price": av_output_price
    }
    update_average_prices(current_date, average_prices)


def update_average_prices(current_date, average_prices):
    # Открываем файл для чтения, если он существует
    try:
        with open("average_prices.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    # Добавляем новые данные с текущей датой
    data[current_date] = average_prices

    # Открываем файл для записи и сохраняем обновленные данные
    with open("average_prices.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

get_data()