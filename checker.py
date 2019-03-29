import json

file = json.load(open('formula.json'))
for x in file:
	if 'stable' in x['bottle']:
		if 'mojave' in x['bottle']['stable']['files']:
			pass
		else:
			#print(json.dumps(x, sort_keys=True, indent=4, separators=(',', ':')))
			print(x['name'])

            
