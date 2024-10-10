from .Models.fireworks import fireworks
from .Models.replicate import replicate
from .Models.novita import novita
from .Models.openrouter import openrouter
from .Models.groq import groq
from .Models.mistral import mistral
from .Models.cohere import cohere
from .Models.openAI import openAI
from .Models.anthropic import anthropic
from .Models.google import google
from .Models.microsoft import microsoft
from .Models.DeepSeek import deepseek
from .Models.CloudFlare import cloudflare
from .Benchmarks.MMLU import MMLU
from .Benchmarks.LLMArena import LLMArena
import concurrent.futures
import time
from datetime import datetime

def __log_service_time__(service, elapsed_time):
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    log_message = f"{current_time} [Info] Service {service} completed in {elapsed_time:.5f} seconds\n"
    with open("log.txt", "a") as log_file:
        log_file.write(log_message)

def parse():
    services = {
        "MMLU": MMLU,
        "LLMArena": LLMArena,
        'openrouter': openrouter,
        'groq': groq,
        'mistral': mistral,
        'cohere': cohere,
        'openAI': openAI,
        'anthropic': anthropic,
        'google': google,
        'microsoft': microsoft,
        'deepseek': deepseek,
        'novita': novita,
        'fireworks': fireworks,
        'replicate': replicate,
        'cloudflare': cloudflare
    }
    result = {}
    print("Start of parsing")
    print('=' * 20)

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(func): name for name, func in services.items()}
        for future in concurrent.futures.as_completed(futures):
            service = futures[future]
            
            service_result, service_elapsed_time = future.result()
            result[service] = service_result
            __log_service_time__(service, service_elapsed_time)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Parsing completed in {elapsed_time:.2f} seconds")

    print('Parsing Success')
    print('=' * 20)
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    with open("log.txt", "a") as log_file:
        log_file.write(f"{current_time} [Success] Parsing Success in {elapsed_time:.2f} seconds\n")
    return result



__all__ = ['parse']