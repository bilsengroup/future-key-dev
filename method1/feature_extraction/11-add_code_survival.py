import pandas as pd
import json
from copy import deepcopy

# load devs_core.csv
devs_core = pd.read_csv('smell-git-mine.csv')
# read the 10-result.json file
with open('10-result.json', 'r') as f:
    devs = json.load(f)

new_features_dict = {'SURVIVAL_RATE': 0}
for dev in devs.values():
    dev.update(deepcopy(new_features_dict))

for row in devs_core.iterrows():
    dev = row[1]
    email = dev['EMAIL']
    CSR = dev['SURVIVAL_RATE']
    found = False

    for dev in devs:
        if email in devs[dev]['devKeys']:
            devs[dev]['SURVIVAL_RATE'] = CSR
            found = True
            break
    if not found:
        print(f'{email} not found')


# save the updated devs dictionary to a new file
with open('11-result.json', 'w') as f:
    json.dump(devs, f)