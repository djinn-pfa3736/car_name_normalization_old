import pandas as pd
import requests
from bs4 import BeautifulSoup

import pdb

url = "https://www.google.co.jp/search"

df = pd.read_csv('convert.csv')

query = ["グーネット", "ゴルフ", "ＧＴＩ ＤＣＣ付き 純正メーカーメモリーナビ"]
search_params = {"q": query}

resp = requests.get(url, params=search_params)
soup = BeautifulSoup(resp.text, "html.parser")
tags = soup.find_all("a")

for tag in tags:
    text = tag.get_text()
    print(text)
