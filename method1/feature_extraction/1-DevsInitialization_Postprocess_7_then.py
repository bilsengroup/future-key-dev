# IMPORTANT
# first run 1-DevsInitialization_Postprocess_6_then.py


import json

#opne 1-devs_pairs_similars.json
with open('1-Devs_pairs_6.json', 'r') as f:
    pairs = json.load(f)

with open("1-Devs_Dictionary_post5.json", "r", encoding="utf-8") as f:
    dev_dict = json.loads(f.read())

# find the chains and the transitive closure
chains = []
new_pairs = []
for pair in pairs:
    new_pair= (pair[1], pair[0])
    new_pairs.append(new_pair)
for pair in new_pairs:
    found = False
    for chain in chains:
        if pair[0] in chain:
            chain.add(pair[1])
            found = True
        elif pair[1] in chain:
            chain.add(pair[0])
            found = True
    if not found:
        chains.append(pair)


# merge the existing developers in the users
# converting sets to lists
for key in dev_dict:
    dev_dict[key]['devKeys'] = set(dev_dict[key]['devKeys'])

for chain in chains:
    chain = list(chain)
    item1 = chain[0]
    for item in chain[1:]:
        item1_info = dev_dict[item1]
        dev_dict[item1]['devKeys'] = dev_dict[item1]['devKeys'].union(set([item]))


            # remove the old developer



# converting sets to lists
for key in dev_dict:
    dev_dict[key]['devKeys'] = list(dev_dict[key]['devKeys'])

with open('1-Devs_Dictionary_post7.json', 'w') as f:
    json.dump(dev_dict, f, indent=4)

