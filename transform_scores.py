import pandas as pd
import numpy as np
import re

in_file = './merged_after_gpa_fix2.tsv'
out_file = './after_score_transform2.tsv'
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

verbal_transform_table = {
    800: 170,
    790: 170,
    780: 170,
    770: 170,
    760: 170,
    750: 169,
    740: 169,
    730: 168,
    720: 168,
    710: 167,
    700: 166,
    690: 165,
    680: 165,
    670: 164,
    660: 164,
    650: 163,
    640: 162,
    630: 162,
    620: 161,
    610: 160,
    600: 160,
    590: 159,
    580: 158,
    570: 158,
    560: 157,
    550: 156,
    540: 156,
    530: 155,
    520: 154,
    510: 154,
    500: 153,
    490: 152,
    480: 152,
    470: 151,
    460: 151,
    450: 150,
    440: 149,
    430: 149,
    420: 148,
    410: 147,
    400: 146,
    390: 146,
    380: 145,
    370: 144,
    360: 143,
    350: 143,
    340: 142,
    330: 141,
    320: 140,
    310: 139,
    300: 138,
    290: 137,
    280: 135,
    270: 134,
    260: 133,
    250: 132,
    240: 131,
    230: 130,
    220: 130,
    210: 130,
    200: 130
}

quantitative_transform_table = {
    800: 166,
    790: 164,
    780: 163,
    770: 161,
    760: 160,
    750: 159,
    740: 158,
    730: 157,
    720: 156,
    710: 155,
    700: 155,
    690: 154,
    680: 153,
    670: 152,
    660: 152,
    650: 151,
    640: 151,
    630: 150,
    620: 149,
    610: 149,
    600: 148,
    590: 148,
    580: 147,
    570: 147,
    560: 146,
    550: 146,
    540: 145,
    530: 145,
    520: 144,
    510: 144,
    500: 144,
    490: 143,
    480: 143,
    470: 142,
    460: 142,
    450: 141,
    440: 141,
    430: 141,
    420: 140,
    410: 140,
    400: 140,
    390: 139,
    380: 139,
    370: 138,
    360: 138,
    350: 138,
    340: 137,
    330: 137,
    310: 136,
    300: 136,
    290: 135,
    280: 135,
    270: 134,
    260: 134,
    250: 133,
    240: 133,
    230: 132,
    220: 132,
    210: 131,
    200: 131
}


def transform_gre(row):
    scores = [float(match.group(1)) for match in number_pattern.finditer(str(row['G']))]
    scores = [score for score in scores if score != 340]
    new_scores = [score for score in scores if 170 >= score >= 130]
    if len(new_scores) >= 1:
        scores = [score for score in scores if 170 >= score]
    if len(scores) == 1 and max(scores) < 1600:
        if scores[0] > 200:
            A = scores[0] % 10
            scores[0] -= A
        else:
            A = 3
        V = scores[0] / 2
        Q = V
    elif len(scores) == 2 and min(scores) <= 5 and max(scores) < 1600:
        V = max(scores) / 2
        Q = V
        A = min(scores)
    elif len(scores) == 2:
        V = min(scores)
        Q = max(scores)
        A = 3
    elif len(scores) == 3:
        sorted_scores = np.sort(scores)
        V = sorted_scores[1]
        Q = sorted_scores[2]
        A = sorted_scores[0]
    else:
        return row

    if Q > 200 and Q % 10 != 0:
        Q += 5
        V -= 5

    if V <= 170 and Q <= 170 and V >= 130 and Q >= 130 and A <= 6:
        V = (V - 130)/40
        Q = (Q - 130)/40
    elif V >= 200 and V <= 800 and Q >= 200 and Q <= 800 and A <= 6:
        if V not in verbal_transform_table or Q not in quantitative_transform_table:
            print('throw')
            return row
        V = (verbal_transform_table[V] - 130)/40#(V - 200)/600
        Q = (quantitative_transform_table[Q] - 130)/40#(Q - 200)/600
    else:
        return row


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