import numpy, pandas
from collections import defaultdict

identities = pandas.read_json('identity-test.json')


# identities.to_csv('output.csv', encoding='utf-8')

assets = pandas.read_json('asset-test.json')

def generateEmailToPubsDict():
	pubsDict = defaultdict(list)
	for i,row in assets.iterrows():
		for name in row['names']: 
			if type(name['email']) == unicode:
				pubsDict[name['email'].lower()].append(row['publication_id'])
	return pubsDict

emailToPubs = generateEmailToPubsDict()

idSets = []
for i,row in identities.iterrows(): 
	emailVal = row['email']
	idSets.append(emailToPubs[emailVal])
	# if type(emailVal) == unicode: 
		

		
identities['publication_ids'] = idSets
identities.reset_index().to_json('enriched_identities.json', orient='records')
