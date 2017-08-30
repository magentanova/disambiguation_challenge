import numpy, pandas
from collections import defaultdict

identities = pandas.read_json('identity-test.json')

assets = pandas.read_json('asset-test-sample-small.json')

def generateSparseNamesDict():
	namesDict = defaultdict(list)
	for i,row in identities.iterrows():
		first,last = row['name'].split(' ')[0], row['name'].split(' ')[1]
		namesDict[first[0].lower() + '_' + last.lower()].append(row)
	return namesDict


sparseNamesDict = generateSparseNamesDict()

ct = 0
for key in sparseNamesDict: 
	if (len(sparseNamesDict[key]) > 1):
		print key, len(sparseNamesDict[key])
		ct += 1 

print ct
# for i,row in assets.iterrows(): 
# 	for nameData in row['names']:


# identities['publication_ids'] = idSets
# identities.reset_index().to_json('identities_enriched_by_field.json', orient='records')
