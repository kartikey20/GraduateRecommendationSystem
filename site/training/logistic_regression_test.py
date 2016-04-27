import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.linear_model
import sklearn.cross_validation

in_file = './after_score_transform.tsv'

data = pd.read_table(in_file, encoding='utf-8')

data = data[data['university'] == "Carnegie Mellon University"]
data = data[data['majors'].map(lambda major: 'CS' in str(major))]
data = data[data['degree'] == 'MS']

data = data[np.isfinite(data['G-V'])]
data = data[np.isfinite(data['G-A'])]
data = data[np.isfinite(data['G-Q'])]
#data = data[np.isfinite(data['T-total'])]
data = data[np.isfinite(data['gpa-normalized'])]

#data.loc[np.isnan(data['G-V']), 'G-V'] = np.mean(data['G-V'])
#data.loc[np.isnan(data['G-A']), 'G-A'] = np.mean(data['G-A'])
#data.loc[np.isnan(data['G-Q']), 'G-Q'] = np.mean(data['G-Q'])
data.loc[np.isnan(data['T-total']), 'T-total'] = np.mean(data['T-total'])
#data.loc[np.isnan(data['gpa-normalized']), 'gpa-normalized'] = np.mean(data['gpa-normalized'])

data['acceptance'] = data['acceptance'].map(lambda x: str(x).lower() in {'ad','offer'})
data['acceptance'] = data['acceptance'].map(lambda x: 1 if x in {'ad','offer'} else x)
data['acceptance'] = data['acceptance'].map(lambda x: 0 if x in {'rej'} else x)


data['top15'] = data['top'].map(lambda x: '15' in str(x))

data['top30'] = np.logical_or(data['top15'], data['top'].map(lambda x: '30' in str(x)))
data['G-QV'] = data['G-Q'] + data['G-V']
#data = data[data['acceptance'] != -1]
#print(data.loc[15000:15100, 'acceptance'])

order = np.arange(data.shape[0])
np.random.shuffle(order)
X = data.as_matrix(['gpa-normalized', 'T-total', 'G-QV', 'top15', 'top30'])[order, :]
y = data.as_matrix([['acceptance']])[order, 0]

print(y[X[:, 2] < 1.3])
print(X[X[:, 2] < 1.3, :])
colors = ['red' if yi else 'blue' for yi in y]
plt.scatter(X[:, -2] + X[:, -1] + X[:, 0], X[:, 2], c=colors, s=80)
plt.show()
logistic_regression = sklearn.linear_model.LogisticRegression()
#logistic_regression.fit(X, y)
print(sklearn.cross_validation.cross_val_score(logistic_regression, X, y, cv=5))