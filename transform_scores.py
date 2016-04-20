import pandas as pd
import numpy as np
import re

in_file = './merged_after_gpa_fix2.tsv'
out_file = './after_score_transform.tsv'
number_pattern = re.compile('[^\d]*(\d+\.?\d*)[^\d]*')

def transform_toefl(row):
    match = number_pattern.finditer(str(row['T']))
    numbers = [float(number.group(1)) for number in match]
    small_numbers = [n for n in numbers if n <= 30]
    large_numbers = [n for n in numbers if n > 30]
    if len(large_numbers) >= 1:
        if min(large_numbers) != 120:
            large_numbers = [n for n in large_numbers if n != 120]

        toefl_score = max(large_numbers)
    elif len(small_numbers) == 4:
        toefl_score = sum(small_numbers)
    else:
        toefl_score = ""
    row['T-total'] = toefl_score

    return row

def transform_gpa(row):
    gpa = float(row['gpa'])
    if gpa is not None:
        if gpa > 8:
            gpa = gpa / 10
        elif gpa > 6:
            gpa = gpa / 8
        elif gpa > 4:
            gpa = gpa / 6
        else:
            gpa = gpa / 4
    row['gpa-normalized'] = gpa
    return row

def transform_gre(row):
    scores = [float(match.group(1)) for match in number_pattern.finditer(str(row['G']))]
    new_scores = [score for score in scores if 170 >= score >= 130]
    if len(new_scores) >= 1:
        scores = [score for score in scores if 170 >= score]
    if len(scores) == 1:
        V = scores[0] / 2
        Q = V
        A = 3
    elif len(scores) == 2 and min(scores) <= 5:
        V = max(scores) / 2
        Q = V
        A = min(scores)
    elif len(scores) == 2:
        V = scores[0]
        Q = scores[1]
        A = 3
    elif len(scores) == 3:
        V = float(scores[0])
        Q = float(scores[1])
        A = float(scores[2])
    else:
        return row
    if V <= 170 and Q <= 170 and V >= 130 and Q >= 130:
        V = (V - 130)/40
        Q = (Q - 130)/40
    elif V >= 200 and V <= 800 and Q >= 200 and Q <= 800:
        V = (V - 200)/600
        Q = (Q - 200)/600

    row['G-V'] = V
    row['G-Q'] = Q
    row['G-A'] = A
    return row



data = pd.read_table(in_file, encoding='utf-8')
data.insert(len(data.columns), 'G-V', "")
data.insert(len(data.columns), 'G-Q', "")
data.insert(len(data.columns), 'G-A', "")
data.insert(len(data.columns), 'gpa-normalized', "")
data.insert(len(data.columns), 'T-total', "")
data = data.apply(transform_gpa, axis='columns') \
           .apply(transform_gre, axis='columns') \
           .apply(transform_toefl, axis='columns')
data.to_csv(out_file, index=False, sep='\t', encoding='utf-8')