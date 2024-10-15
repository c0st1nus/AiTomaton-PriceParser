import json
from datetime import datetime
import parsers
import re
import handler

def get_data():
    consolidated_data = consolidate_data(parsers.parse())
    handler.save_data(consolidated_data, calculate_average_prices(consolidated_data))

def log_success(service):
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    log_message = f"{current_time} [Success] The {service} has been parsed\n"
    with open("log.txt", "a") as log_file:
        log_file.write(log_message)

def consolidate_data(data):
    consolidated_data = {}
    for providers, models in data.items():
        for model_name, provider in models.items():
            clean_column = clean_column_name(model_name)
            real_model_name = search_model(clean_column)
            if real_model_name == 'SKIP':
                continue
            if real_model_name is None:
                print(clean_column)
                continue
            try:
                if providers == "MMLU" or providers == "LLMArena":
                    if real_model_name not in consolidated_data:
                        consolidated_data[real_model_name] = {}
                    consolidated_data[real_model_name][providers] = {
                        "value": data[providers][model_name]
                    }
                else:
                    if real_model_name not in consolidated_data:
                        consolidated_data[real_model_name] = {}
                    consolidated_data[real_model_name][providers] = {
                        "input_price": str(round(float(data[providers][model_name]["input_price"]), 4)),
                        "output_price": str(round(float(data[providers][model_name]["output_price"]), 4))
                    }
            except ValueError:
                consolidated_data[real_model_name][providers] = {
                    "input_price": str(round(float(data[providers][model_name]["input_price"].replace(',', '.')), 4)),
                    "output_price": str(round(float(data[providers][model_name]["output_price"].replace(',', '.')), 4))
                }
    return consolidated_data

def search_model(model_name):
    filters = json.load(open("filter.json", 'r', encoding="UTF-8"))
    for key, models in filters.items():
        if model_name in models:
            return str(key)
    return None

def clean_column_name(name):
    if not name:
        return None
    name = re.sub(r'[^0-9a-zA-Z_]', '_', name)
    if name[0].isdigit():
        name = 'col_' + name
    return name

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