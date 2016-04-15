import pandas as pd

original_path = './grad_data_all-refined.tsv' #take names from here
to_fix_path = './after_university_split.tsv'
fixed_path = './after_university_split_fixed.tsv'

original = pd.read_table(original_path,encoding='utf-8')
names = {}
for i, row in original.iterrows():
    assert row['url'] not in names or names[row['url']] == row['user']
    names[row['url']] = row['user']


def replace_name(row):
    row['user'] = names[row['url']]
    return row


data_to_fix = pd.read_table(to_fix_path, encoding='utf-8')
fixed_data = data_to_fix.apply(replace_name, axis='columns')
fixed_data.to_csv(fixed_path, index=False, sep='\t', encoding='utf-8')

