from parsers import *
from datetime import datetime
import json

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

        # Log final success message
        print('Parsing Succes')
        print('=' * 20)
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
        with open("log.txt", "a") as log_file:
            log_file.write(f"{current_time} [Success] Parsing Success\n")

        # Save result to result.json
        with open("result.json", "w") as result_file:
            json.dump(result, result_file, indent=4)

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

# Вызов функции get_data()
get_data()