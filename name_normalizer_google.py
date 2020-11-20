import pandas as pd
import requests
from bs4 import BeautifulSoup

import pdb

url = "https://www.google.co.jp/search"

df = pd.read_csv('convert.csv')

ZEN = "".join(chr(0xff01 + i) for i in range(94))
HAN = "".join(chr(0x21 + i) for i in range(94))

ZEN2HAN = str.maketrans(ZEN, HAN)
HAN2ZEN = str.maketrans(HAN, ZEN)

answer = []
normalized = []
for i in range(len(df)):
    car_name = df.iloc[i, 3]
    grade = df.iloc[i, 4]
    answer.append(df.iloc[i, 9])

    query1 = ["グーネット", car_name]
    search_params1 = {"q": query1}

    resp1 = requests.get(url, params=search_params1)
    soup1 = BeautifulSoup(resp1.text, "html.parser")
    tags1 = soup1.find_all("a")

    query2 = ["グーネット", car_name, grade]
    search_params2 = {"q": query2}

    resp2 = requests.get(url, params=search_params2)
    soup2 = BeautifulSoup(resp2.text, "html.parser")
    tags2 = soup2.find_all("a")

    print(':::' + car_name + ':::')
    candidates = []
    for tag in tags1:
        text = tag.get_text()
        if "goo-net" in text:
            end_pos = text.find("（")
            if end_pos != -1:
                candidates.append(text[0:end_pos])

    for tag in tags2:
        text = tag.get_text()
        if "goo-net" in text:
            end_pos = text.find("（")
            if end_pos != -1:
                candidates.append(text[0:end_pos])

    idx = 0
    print(candidates)
    for i in range(len(candidates)):
        if len(candidates) == len(car_name):
            idx = i
            break

    normalized_name = candidates[idx]
    normalized_name = normalized_name.translate(HAN2ZEN)
    normalized_name = normalized_name.replace('−', '－')
    normalized.append(normalized_name)

for i in range(len(answer)):
    if answer[i] != normalized[i]:
        print(answer[i] + ":" + normalized[i])

pdb.set_trace()
