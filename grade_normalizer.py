import numpy as np

import pandas as pd
import MeCab
from io import StringIO

import pdb

def normalize_term(term):

    term = term.replace('\u3000', ' ')

    return(term)
def compare_terms(term1, term2):
    if len(term2) < len(term1):
        tmp = term1
        term1 = term2
        term2 = tmp

    match_level = 0

    if term1 in term2:
        match_level += len(term1)/len(term2)
    else:
        pos1 = 0
        pos2_start = 0
        gap_len = 0
        while pos1 < len(term1):
            pos2 = pos2_start
            while pos2 < len(term2):
                if term1[pos1] == term2[pos2]:
                    match_level += 1/(len(term2) + gap_len)
                    pos2 += 1
                    gap_len = 0
                    pos2_start = pos2
                    break
                gap_len += 1
                pos2 += 1
            pos1 += 1

    return match_level

def compare_grade_name(grade_name, proto_name):
    normalized_grade_name = normalize_term(grade_name)
    normalized_proto_name = normalize_term(proto_name)

    match_level = 0

    tmp1 = normalized_grade_name.split(' ')
    tmp2 = normalized_proto_name.split(' ')

    for term1 in tmp1:
        for term2 in tmp2:
            match_level += compare_terms(term1, term2)

    if (grade_name == '２．０　ＧＴ　リミテッド　ナビ・バックカメラ・ＥＴＣ') and (proto_name == 'ＧＴリミテッド'):
    # if (grade_name == '６６０ Ｇ メイクアップ ＳＡＩＩ ナビ ドラレコ 衝突被害軽減ブレーキ') and (proto_name == 'Ｇメイクアップ ＳＡⅡ'):
        pdb.set_trace()

    if match_level == 0:
        return -1, -1
    else:
        return proto_name, match_level

df = pd.read_csv("./convert.csv")

proto_name_vec = []
for grade_name in df['PROTOグレード名']:
    if (grade_name not in proto_name_vec) and not (grade_name != grade_name):
        proto_name_vec.append(grade_name)

matched_name_vec = []
for grade_name in df['先方側グレード名']:
    matched_flag = False
    candidate_vec = []
    match_level_vec = []
    for proto_name in proto_name_vec:
        result, match_level = compare_grade_name(grade_name, proto_name)
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

for i in range(len(df)):
    if matched_name_vec[i] != df.iloc[i,11]:
        print((matched_name_vec[i], df.iloc[i, 11]))

pdb.set_trace()
