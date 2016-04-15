import pandas as pd
import re

in_file = './before_university_split.tsv'
out_file = './after_university_split.tsv'

data = pd.read_table(in_file, encoding='utf-8')
result = pd.DataFrame(columns=data.columns)

print(data.shape)
for i, row in data.iterrows():
    if i % 100 == 0:
        print(i)
    universities = [u.strip() for u in str(row['university']).split(',')]
    for university in universities:
        new_row = row.copy()
        match_acceptance = re.match("([^\(]*)\(([^\(]*)\)", university)
        if match_acceptance is not None:
            new_row['acceptance'] = match_acceptance.group(2)
            university = match_acceptance.group(1)
        new_row['university'] = university
        result = result.append(new_row, ignore_index=True)


result.to_csv(out_file, index=False, sep='\t', encoding='utf-8')
print(result.shape)
