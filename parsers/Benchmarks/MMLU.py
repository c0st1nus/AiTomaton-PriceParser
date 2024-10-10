import requests
from bs4 import BeautifulSoup
import json
import time
import re

def clean_column_name(name):
        if not name:
            return None
        name = re.sub(r'[^0-9a-zA-Z_]', '_', name)
        if name[0].isdigit():
            name = 'col_' + name
        return name

def MMLU():
    start_time = time.time()
    result = {}
    url = "https://paperswithcode.com/sota/multi-task-language-understanding-on-mmlu"
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    script_tag = soup.select_one('#evaluation-table-data')
    data = {}
    if script_tag:
        json_data = script_tag.string.strip()
        data = json.loads(json_data)
    for item in data:
        result[clean_column_name(item["method"])] = str(item["metrics"]["Average (%)"]) + '%'
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time

if __name__ == "__main__":
    print(MMLU())