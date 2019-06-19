import json
import urllib.request

url = "https://formulae.brew.sh/api/formula.json"


file = json.load(urllib.request.urlopen(url))
for x in file:
    if 'stable' in x['bottle']:
        if 'mojave' in x['bottle']['stable']['files']:
            pass
        else:
            #print(json.dumps(x, sort_keys=True, indent=4, separators=(',', ':')))
            print(x['name'])
