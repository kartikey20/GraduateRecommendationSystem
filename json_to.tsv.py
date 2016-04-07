import json;
import os;

data_root = "data/";
data_files = os.listdir(data_root);

tsv_file = open('grad_data_all.tsv', "w+");

columns = ['user', 'url', 'gpa', 'year', 'degree', 'acceptance', 'university', 'majors', 'G', 'T', 'top']
columnsCount = {};

for i in range(0, len(columns)):
	columnsCount[columns[i]] = 0;
	if i != len(columns) - 1:
		tsv_file.write(columns[i] + "\t");
	else:
		tsv_file.write(columns[i] + "\n");

for file_name in data_files:
	print('openining file: ' + file_name);
	f = open(data_root + file_name, 'r');
	file_content = f.readlines()[0]
	file_json_str = '[%s]'%file_content.replace('}{', '}, {');
	file_json = json.loads(file_json_str);
	print('Going through ' + str(len(file_json)) + ' objects');
	for json_obj in file_json:
		for i in range(0, len(columns)):
			if columns[i] in json_obj and len(json_obj[columns[i]]) > 0:
                                columnsCount[columns[i]] = columnsCount[columns[i]] + 1;
			if i != len(columns) - 1:
				if columns[i] in json_obj:
					tsv_file.write(str(json_obj[columns[i]]) + "\t");
				else:
					tsv_file.write("" + "\t");
			else:
				if columns[i] in json_obj:
					tsv_file.write(str(json_obj[columns[i]]) + "\n");
				else:
					tsv_file.write("" + "\n");
	print('completed file ' + file_name);
print(columnsCount);

tsv_file.flush();
tsv_file.close();
