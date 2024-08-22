# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'
}

def groq(url="https://wow.groq.com/"):
    # РџРѕР»СѓС‡РµРЅРёРµ HTML-РєРѕРґР° СЃС‚СЂР°РЅРёС†С‹
    response = requests.get(url, headers=headers)
    html_content = response.text

    # РџР°СЂСЃРёРЅРі HTML-РєРѕРґР° СЃ РїРѕРјРѕС‰СЊСЋ BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # РџРѕРёСЃРє С‚Р°Р±Р»РёС†С‹ СЃ РєР»Р°СЃСЃРѕРј 'pmatrix'
    table = soup.find('table', class_='pmatrix')

    # РџСЂРѕРІРµСЂРєР°, С‡С‚Рѕ С‚Р°Р±Р»РёС†Р° РЅР°Р№РґРµРЅР°
    if table is None:
        return {}

    # Р�РЅРёС†РёР°Р»РёР·Р°С†РёСЏ СЃР»РѕРІР°СЂСЏ РґР»СЏ С…СЂР°РЅРµРЅРёСЏ РґР°РЅРЅС‹С…
    data = {}

    # Р РµРіСѓР»СЏСЂРЅРѕРµ РІС‹СЂР°Р¶РµРЅРёРµ РґР»СЏ РёР·РІР»РµС‡РµРЅРёСЏ С‡РёСЃР»РѕРІРѕР№ С‡Р°СЃС‚Рё С†РµРЅС‹
    price_pattern = re.compile(r'\$([\d.]+)')

    # Р�Р·РІР»РµС‡РµРЅРёРµ РґР°РЅРЅС‹С… РёР· С‚Р°Р±Р»РёС†С‹
    for row in table.find('tbody').find_all('tr'):
        columns = row.find_all('td')
        model = columns[0].text.strip()
        speed = columns[1].text.strip()
        
        price_text = columns[2].text.strip()
        prices = price_pattern.findall(price_text)
        
        if len(prices) == 2:
            input_price, output_price = prices
        else:
            input_price = prices[0]
            output_price = None
        
        data[model] = {
            "input_price": input_price,
            "output_price": output_price
        }

    return data

# РџСЂРёРјРµСЂ РІС‹Р·РѕРІР° С„СѓРЅРєС†РёРё
if __name__ == "__main__":
    result = groq()
    print(result)