import json
import os
import sys
import urllib.request
import ssl
from argparse import ArgumentParser

macos_ver = {"sierra": 16, "high_sierra": 17,
             "mojave": 18, "catalina": 19, "big_sur": 20,
             "monterey": 21}
# macOS Kernel version Darwin


def get_sysname():
    if sys.platform.startswith('darwin'):
        for name, ver in macos_ver.items():
            if int(os.uname().release.split('.', maxsplit=1)[0]) == ver:
                return name
    else:
        return os.name


parser = ArgumentParser(description="check compatibility")
parser.add_argument(
    '--target', '-t', choices=["sierra", "high_sierra", "mojave", "catalina", "big_sur", "monterey"], default=get_sysname())
# parser.add_argument('--reactions', '-r', action="store_true")
arguments = parser.parse_args()


url = "https://formulae.brew.sh/api/formula.json"
count = 0

file = json.load(urllib.request.urlopen(url, context=ssl.SSLContext(ssl.PROTOCOL_TLS)))
for x in file:
    if 'stable' in x['bottle']:
        if arguments.target in x['bottle']['stable']['files']:
            pass
        else:
            #print(json.dumps(x, sort_keys=True, indent=4, separators=(',', ':')))
            # print(x['name'])
            count += 1
print(count, "incompatible formulae")
