import pandas as pd
import numpy as np

#Input
rank_preference = 0.6
cost_preference = 0.4


objective = 'linear'

def normalize(series):
    return (series - series.min())/(series.max() - series.min())


data = pd.read_table('main-data.tsv', encoding='utf-8')
data['QSscore'] = data['QSscore'].convert_objects(convert_numeric=True)
data['cost'] = data['cost'].convert_objects(convert_numeric=True)
data = data[np.isfinite(data['QSscore'])]
data = data[np.isfinite(data['cost'])]
data['cost_normalized'] = 1-normalize(data['cost'])
data['Qsscore_normalized'] = normalize(data['QSscore'])
data = data.groupby('university').mean()

if objective == 'linear':
    data['sort-criterium'] = cost_preference * data['cost_normalized'] + rank_preference * data['Qsscore_normalized']
elif objective == 'exponential':
    data['sort-criterium'] = cost_preference * np.exp(data['cost_normalized']) + \
                             rank_preference * np.exp(data['Qsscore_normalized'])
elif objective == 'exponential-score':
    data['Qsscore_normalized'] = normalize(np.exp(data['Qsscore_normalized']))
    data['sort-criterium'] = cost_preference * data['cost_normalized'] + \
                             rank_preference * data['Qsscore_normalized']
elif objective == 'squared':
    data['sort-criterium'] = cost_preference * data['cost_normalized']**2 + \
                             rank_preference * data['Qsscore_normalized']**2
elif objective == 'squared-score':
    data['sort-criterium'] = cost_preference * data['cost_normalized'] + \
                             rank_preference * data['Qsscore_normalized']**2
elif objective == 'squared-weight':
    data['sort-criterium'] = cost_preference**2 * data['cost_normalized'] + \
                             rank_preference**2 * data['Qsscore_normalized']
elif objective == 'linear-offset':
    data['sort-criterium'] = cost_preference * (data['cost']/data['cost'].max()) + rank_preference * data['Qsscore_normalized']


data = data.sort('sort-criterium', ascending=False)[['QSscore', 'qsrank', 'cost', 'sort-criterium', 'admission rate']]

#Output
for i, (university, (QSscore, qsrank, cost, admission_rate, sort_criterium)) in enumerate(data.iterrows()):
    if i > 10:
        break
    print("%s: %f %f(%d) = %f - %f" % (university, cost, QSscore, qsrank, sort_criterium, admission_rate))
