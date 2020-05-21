import sys
import json

def process(pluginList):
    for p in pluginList:
        name = p["name"].strip()
        version = p["version"]
        if version is None:
            version = ""
        else:
            version = version.strip()
        technology = p["technology"].strip()
        vendor = p["vendor"].strip()
        category = p["category"].strip()
        caps = p["caps"].strip()
        if len(version) > 0:
            name = name + " v" + version
        # fix some null entry problems with VST3s and generally clean things up
        if len(version) > 0:
            version = "v" + version
        if "VST2" in technology:
            technology = "VST2"
        if "VST3" in technology:
            technology = "VST3"
        print(f'{name:48s} {technology:8s} {category:12s} {vendor:40s} {caps:40s}')

args = sys.argv[1:]

if len(args) != 1:
    print("Usage: VSTList <Cantabile plugin list file name>")
    exit(1)

fn = args[0]

# fn = 'C:\\Users\\Warren\\AppData\\Local\\Topten Software\\Cantabile 3.0 (VST_Testing)\\plugins.json'
# fn = 'C:\\Users\\Warren\\AppData\\Local\\Topten Software\\Cantabile 3.0\\plugins.json'

with open(fn, 'r') as f:
    data = json.load(f)

data.sort(key = lambda x: str(x["name"]).lower())
# data.sort(key = lambda x: str(x["vendor"]).lower())

# group plugins by type

synths = []
effects = []
others = []

for p in data:
    # skip non-VST .dlls
    if p["name"] is not None:
        if p["category"] == "Synth":
            synths.append(p)
        elif p["category"] == "Effect":
            effects.append(p)
        else:
            others.append(p)

if len(synths) > 0:
    process(synths)
    print()

if len(effects) > 0:
    process(effects)
    print()

if len(others) > 0:
    process(others)
    print()

pluginCount = len(synths) + len(effects) + len(others)

print(f'{pluginCount} plugin(s) - {len(synths)} synths, {len(effects)} effects, {len(others)} others')
