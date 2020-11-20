import numpy as np

import pandas as pd
import MeCab
from io import StringIO

import pdb

m = MeCab.Tagger('-O chasen -u /usr/lib/mecab/dic/original/car_name.dic')

def normalize_term(term):
    term = term.replace('Ｊｅｅｐ', 'ジープ')
    term = term.replace('ミニ', 'ＭＩＮＩ')
    return(term)

def compare_car_name(car_name, proto_name):
    normalized_car_name = normalize_term(car_name)
    normalized_proto_name = normalize_term(proto_name)
    if normalized_car_name == normalized_proto_name:
        return proto_name, len(car_name)*2

    # elif (normalized_car_name in normalized_proto_name) or (normalized_proto_name in normalized_car_name):
    elif normalized_car_name in normalized_proto_name:
        return proto_name, len(car_name)
    else:
        analyzed = m.parse(normalized_car_name)
        df_car_name = pd.read_csv(StringIO(analyzed), delimiter='\t', names=['単語', '読み','原形', '品詞', '活用', '活用形'])
        analyzed = m.parse(normalized_proto_name)
        df_proto_name = pd.read_csv(StringIO(analyzed), delimiter='\t', names=['単語', '読み','原形', '品詞', '活用', '活用形'])

        matched_dic = {}
        for term in df_car_name['単語']:
            if (term == '－') or (term == 'EOS'):
                continue

            for proto_term in df_proto_name['単語']:

                if term in proto_term:
                    if proto_term in matched_dic:
                        matched_dic[proto_term] += 1
                    else:
                        matched_dic[proto_term] = 1

        if len(matched_dic.keys()) < 1:
            return -1, -1
        else:
            return max(matched_dic), matched_dic[max(matched_dic)]

df = pd.read_csv("./convert.csv")

proto_name_vec = []
for car_name in df['PROTO車種名']:
    if car_name not in proto_name_vec:
        proto_name_vec.append(car_name)

matched_name_vec = []
for car_name in df['先方側車種名']:
    matched_flag = False
    candidate_vec = []
    match_level_vec = []
    for proto_name in proto_name_vec:
        result, match_level = compare_car_name(car_name, proto_name)
        if result is not -1:
            # matched_name_vec.append(result)
            candidate_vec.append(result)
            match_level_vec.append(match_level)
            matched_flag = True

    candidate_vec = np.array(candidate_vec)

    if not matched_flag:
        matched_name_vec.append('登録不可')
    else:
        max_idx = np.argmax(match_level_vec)
        matched_name_vec.append(candidate_vec[max_idx])

    """
    else:
        if len(match_level_vec) == 1:
            complete_match = (match_level_vec[0] == 1)
        else:
            complete_match = np.where(match_level_vec == 1, True, False)

        if len(match_level_vec) == 1 and complete_match:
            matched_name_vec.append(candidate_vec[0])
        elif np.sum(complete_match) != 0:
            matched_name_vec.append(candidate_vec[complete_match].tolist())
        else:
            matched_name_vec.append(candidate_vec[0])
    """
for i in range(len(df)):
    if matched_name_vec[i] != df.iloc[i,9]:
        print((matched_name_vec[i], df.iloc[i, 9]))

pdb.set_trace()
