import pandas as pd
import numpy as np
import pickle


objective = 'linear'

def normalize(series):
    return (series - series.min())/(series.max() - series.min())

def create_list(gre_q, gre_v, gre_w, toefl, ranking, gpa, major, rank_preference, cost_preference):
    acceptance_preference = 0.1
    with open('../data/trained_models', 'rb') as f:
        classifiers = pickle.load(f)

    gpa = gpa/4
    gre_q = (gre_q - 130)/40
    gre_v = (gre_v - 130)/40
    undergrad_in_top15 = ranking <= 15
    undergrad_in_top30 = ranking <= 30

    data = pd.read_table('../data/main-data.tsv', encoding='utf-8')
    data['QSscore'] = data['QSscore'].convert_objects(convert_numeric=True)
    data['cost'] = data['cost'].convert_objects(convert_numeric=True)
    data = data[np.isfinite(data['QSscore'])]
    data = data[np.isfinite(data['cost'])]
    data['cost_normalized'] = 1-normalize(data['cost'])
    data['Qsscore_normalized'] = normalize(data['QSscore'])

    data = data.groupby('university').max()
    data['chance'] = data.index.map(lambda univ: 0 if (major, univ) not in classifiers else classifiers[major, univ].predict_proba([gre_v, gre_q, gre_w, gpa, toefl, undergrad_in_top15, undergrad_in_top30, gre_v + gre_q])[0, 1])

    if objective == 'linear':
        data['sort-criterium'] = cost_preference * data['cost_normalized'] + rank_preference * data['Qsscore_normalized'] + acceptance_preference * data['chance']
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


    data = data.sort('sort-criterium', ascending=False)[['QSscore', 'qsrank', 'cost', 'sort-criterium', 'admission rate', 'url', 'chance']]

    #Output
    res = [];
    for i, (university, (QSscore, qsrank, cost, admission_rate, sort_criterium, url, chance)) in enumerate(data.iterrows()):
        
        if i > 10:
            break
        #print("%s: %f %f(%d) = %f - %f" % (university, cost, QSscore, qsrank, sort_criterium, admission_rate))
        row = {'university' : university,
               'cost' : cost,
               'chance' : chance,
               'url' : url,
               'ranking' : qsrank};

        res.append(row);

    return res;

if __name__ == '__main__':
    create_list(170, 170, 6, 100, 1, 4.0, 'CS', 0.4, 0.6)
