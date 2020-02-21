import json
from argparse import ArgumentParser
import urllib.request


parser = ArgumentParser(description="check compatibility")
parser.add_argument(
    '--input', '-in', choices=["sierra", "high_sierra", "mojave", "catalina"], default="mojave")
# parser.add_argument('--reactions', '-r', action="store_true")
arguments = parser.parse_args()


url = "https://formulae.brew.sh/api/formula.json"


file = json.load(urllib.request.urlopen(url))
for x in file:
    if 'stable' in x['bottle']:
        if arguments.input in x['bottle']['stable']['files']:
            pass
        else:
            #print(json.dumps(x, sort_keys=True, indent=4, separators=(',', ':')))
            print(x['name'])
