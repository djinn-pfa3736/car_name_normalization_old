import pandas as pd
import numpy as np

def calc_cost(word):
    cost = np.floor(np.max((-32768, -400*len(word)**1.5)))
    return cost

df = pd.read_csv("convert.csv")

car_grade = []
for i in range(len(df)):
    if not (df.iloc[i,11] != df.iloc[i,11]):
        tmp = df.iloc[i,11].split(' ')
        if df.iloc[i,11] not in car_grade:
            print("{},0,0,{},車名,*,*,*,*,*,{},{},{}".format(df.iloc[i,11], -30000, df.iloc[i,11], df.iloc[i,11], df.iloc[i,11]))
            car_grade.append(df.iloc[i,11])
        for j in range(len(tmp)):
            if tmp[j] not in car_grade:
                # print("{},0,0,{},車名,*,*,*,*,*,{},{},{}".format(df.iloc[i,9], calc_cost(df.iloc[i,9]), df.iloc[i,9], df.iloc[i,9], df.iloc[i,9]))
                print("{},0,0,{},車名,*,*,*,*,*,{},{},{}".format(tmp[j], -30000, tmp[j], tmp[j], tmp[j]))
                car_grade.append(tmp[j])
