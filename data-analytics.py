from __future__ import print_function
import pandas;

columns = ['user', 'url', 'gpa', 'Year', 'Semester', 'degree', 'acceptance', 'university', 'majors', 'G', 'T', 'top']
filename = 'data/grad_data_all-refined.tsv';
grads = pandas.read_table(filename, "\t", header=0);

print('Unique Attributes: \n');
for column in columns:
    print(column, str(len(grads[column].unique())) + "\n");
