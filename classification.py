import pandas as pd
import numpy as np
import json
from sklearn import cross_validation
from sklearn import svm
import pickle


in_file = 'main-data.tsv' #from github
data = pd.read_table(in_file, encoding='utf-8')
#data = data[np.isfinite(data['gpa-norm'])]
#data = data[np.isfinite(data['G-V'])]
#data = data[np.isfinite(data['G-A'])]
#data = data[np.isfinite(data['G-Q'])]
data.loc[np.isnan(data['gpa-norm']), 'gpa-norm'] = np.mean(data['gpa-norm'])
data.loc[np.isnan(data['G-V']), 'G-V'] = np.mean(data['G-V'])
data.loc[np.isnan(data['G-A']), 'G-A'] = np.mean(data['G-A'])
data.loc[np.isnan(data['G-Q']), 'G-Q'] = np.mean(data['G-Q'])
data.loc[np.isnan(data['toefl']), 'toefl'] = np.mean(data['toefl'])
#data = data[np.isfinite(data['toefl'])]
data['acceptance'] = data['acceptance'].map(lambda x: str(x).lower() in {'ad','offer'})
data['acceptance'] = data['acceptance'].map(lambda x: 1 if x in {'ad','offer'} else x)
data['acceptance'] = data['acceptance'].map(lambda x: 0 if x in {'rej'} else x)
data['top15'] = data['top'].map(lambda x: '15/211' in str(x))
data['top30'] = np.logical_or(data['top15'], data['top'].map(lambda x: '30/211' in str(x)))
data['G-QV'] = data['G-Q'] + data['G-V']

classifiers = {}

for major in np.unique(data['major'].astype(str)):

    for university in np.unique(data['university']):


        dt = data[(data['university'] == university)&(data['major'] == major)]
        if dt.size > 18 & np.unique(dt['acceptance']).size >1 :# can define data size limit requirment here
            print("%s: %s" % ( major, university))
            ad = dt[dt['acceptance'] ]
            ad[['G-V','G-Q', 'G-A', 'gpa-norm', 'toefl', 'G-QV']] = ad[['G-V','G-Q', 'G-A', 'gpa-norm', 'toefl', 'G-QV']].fillna(ad[['G-V','G-Q', 'G-A', 'gpa-norm', 'toefl', 'G-QV']].mean())#replace na by mean
            rej = dt[~dt['acceptance']]
            rej[['G-V','G-Q', 'G-A', 'gpa-norm', 'toefl', 'G-QV']] = rej[['G-V','G-Q', 'G-A', 'gpa-norm', 'toefl', 'G-QV']].fillna(rej[['G-V','G-Q', 'G-A', 'gpa-norm', 'toefl', 'G-QV']].mean())
            dt = pd.concat([ad, rej], ignore_index=False)
            dt.iloc[np.random.permutation(len(dt))]
            classifier = svm.SVC(C=1.2, probability=True, class_weight='auto')##feel free to tackle parameters
            classifier.fit(dt[['G-V', 'G-Q', 'G-A', 'gpa-norm', 'toefl',  'top15', 'top30', 'G-QV']],dt['acceptance'])
            #then we can use classifier.predict(['G-V', 'G-Q', 'G-A', 'gpa-norm', 'toefl',  'top15', 'top30', 'G-QV'])
            #uni.update({"%s" %university : classifier})
            classifiers[(major, university)] = classifier
    #mj.update({"%s" %major : uni}) # in json format but not dump
#return json.dumps(mj) # feel free to correct the code

with open('trained_models', 'wb') as f:
    pickle.dump(classifiers, f)