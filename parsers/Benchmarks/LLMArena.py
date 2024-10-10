import re
import json
import time
import requests

def clean_column_name(name):
        if not name:
            return None
        name = re.sub(r'[^0-9a-zA-Z_]', '_', name)
        if name[0].isdigit():
            name = 'col_' + name
        return name

def LLMArena():
    start_time = time.time()
    result = {}
    response = requests.get("https://lmsys-chatbot-arena-leaderboard.hf.space/")
    content = response.text

    pattern = re.compile(r'<script>window\.gradio_config\s*=\s*(\{.*?\});<\/script><script>window\.gradio_api_info\s*=', re.DOTALL)

    match = pattern.search(content)
    if match:
        json_data = match.group(1)
        data = json.loads(json_data)

    pattern = re.compile(r'>(.*?)<\/a>')

    for item in data['components'][18]['props']['value']['data']:
        model_info = item[1]
        banch = item[2]
        match = pattern.search(model_info)
        if match:
            model_name = match.group(1)
            result[clean_column_name(model_name)] = banch
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time
if __name__ == "__main__":
    LLMArena()