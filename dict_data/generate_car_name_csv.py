import pandas as pd
import numpy as np

def calc_cost(word):
    cost = np.floor(np.max((-32768, -400*len(word)**1.5)))
    return cost

df = pd.read_csv("convert.csv")

car_name = []
for i in range(len(df)):
    if df.iloc[i,9] not in car_name:
        # print("{},0,0,{},車名,*,*,*,*,*,{},{},{}".format(df.iloc[i,9], calc_cost(df.iloc[i,9]), df.iloc[i,9], df.iloc[i,9], df.iloc[i,9]))
        print("{},0,0,{},車名,*,*,*,*,*,{},{},{}".format(df.iloc[i,9], -32768, df.iloc[i,9], df.iloc[i,9], df.iloc[i,9]))
        car_name.append(df.iloc[i,9])
