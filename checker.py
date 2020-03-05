import json
from argparse import ArgumentParser
import urllib.request
import os

macos_ver = {"sierra": 16, "high_sierra": 17, "mojave": 18, "catalina": 19}
# macOS Kernel version Darwin

def get_sysname():
    for name, ver in macos_ver.items():
        if int(os.uname().release.split('.', maxsplit=1)[0]) == ver:
            return name


parser = ArgumentParser(description="check compatibility")
parser.add_argument(
    '--target', '-t', choices=["sierra", "high_sierra", "mojave", "catalina"], default=get_sysname())
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
