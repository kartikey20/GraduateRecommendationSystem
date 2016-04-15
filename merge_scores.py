import pandas as pd
import numpy as np

in_file = './grad_data_all-refined.tsv'
out_file = './grad_data_all-merged_gpa.tsv'

data = pd.read_table(in_file)


def merge_scores(indices):
    for user in indices:
        if user % 1000 == 0:
            print(user)
        filter_key = data['user'] == data['user'][user]
        user_data = data[filter_key]

        gpa = float('nan')
        gre = float('nan')
        toefl = float('nan')
        for i, row in user_data.iterrows():
            if type(row['gpa']) is str or not np.isnan(row['gpa']):
                gpa = row['gpa']
            if type(row['G']) is str or not np.isnan(row['G']):
                gre = row['G']
            if type(row['T']) is str or not np.isnan(row['T']):
                toefl = row['T']

        for i, row in user_data.iterrows():
            data.loc[i, 'gpa'] = gpa
            data.loc[i, 'G'] = gre
            data.loc[i, 'T'] = toefl


merge_scores(range(data.shape[0]))

data.to_csv(out_file, index=False, sep='\t')

