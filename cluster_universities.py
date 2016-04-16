import pandas;
import re;
import collections;

data = pandas.read_table('ravishpart.tsv', '\t');
universities = data['university'];
univertity_map = {};
file_out = 'cluster_out.txt';
fp = open(file_out, 'w+');

for row in universities:
	univ_values = re.split(''',(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', row);
	for univ in univ_values:
		univ_norm = univ.lower().strip().encode('utf-8');
		if univ_norm not in univertity_map:
			univertity_map[univ_norm] = 0;
		univertity_map[univ_norm] = univertity_map[univ_norm] + 1;

length = len(univertity_map);
print(str(length));

od = collections.OrderedDict(sorted(univertity_map.items()));

for row in od:
	fp.write(str(row.decode('utf-8')) + " : " + str(od[row]) + "\n");

fp.flush();
fp.close();