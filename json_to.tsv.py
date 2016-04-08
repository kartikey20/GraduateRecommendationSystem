import json;
import os;
import operator;

data_root = "data/";
data_files = os.listdir(data_root);

#tsv_file = open('grad_data_all.tsv', "w+");

columns = ['user', 'url', 'gpa', 'year', 'degree', 'acceptance', 'university', 'majors', 'G', 'T', 'top']
columnsCount = {};
uniqueUsers = {};
uniqueUnivs = {};

for i in range(0, len(columns)):
    columnsCount[columns[i]] = 0;
    if i != len(columns) - 1:
        #tsv_file.write(columns[i] + "\t");
        pass;
    else:
        #tsv_file.write(columns[i] + "\n");
        pass;

for file_name in data_files:
    #print('openining file: ' + file_name);
    f = open(data_root + file_name, 'r');
    file_content = f.readlines()[0]
    file_json_str = '[%s]'%file_content.replace('}{', '}, {');
    file_json = json.loads(file_json_str);
    #print('Going through ' + str(len(file_json)) + ' objects');
    for json_obj in file_json:
            for i in range(0, len(columns)):
                if columns[i] in json_obj and len(json_obj[columns[i]]) > 0:
                    columnsCount[columns[i]] = columnsCount[columns[i]] + 1;
                '''
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
                '''
    
            if json_obj['user'] not in uniqueUsers:
                uniqueUsers[json_obj['user']] = 0;
            uniqueUsers[json_obj['user']] = uniqueUsers[json_obj['user']] + 1;

            if 'university' in json_obj:
                if json_obj['university'] not in uniqueUnivs:
                    uniqueUnivs[json_obj['university']] = 0;
                uniqueUnivs[json_obj['university']] = uniqueUnivs[json_obj['university']] + 1;
    #print('completed file ' + file_name);

sortedUsers = sorted(uniqueUsers.items(), key=operator.itemgetter(1))
sortedUnivs = sorted(uniqueUnivs.items(), key=operator.itemgetter(1))
print(columnsCount);
print(len(uniqueUsers));
print(len(uniqueUnivs));

for i in range(len(sortedUnivs) - 10, len(sortedUnivs)):
    print(sortedUnivs[i]);

#tsv_file.flush();
#tsv_file.close();
