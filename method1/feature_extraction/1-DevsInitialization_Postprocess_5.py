import json

#opne 1-devs_pairs_similars.json
with open('1-Devs_Pairs_similars.json', 'r') as f:
    pairs = json.load(f)
with open('1-Devs_Pairs_similars_test.json', 'r') as f:
    pairs = json.load(f)


with open("1-Devs_Dictionary_post3.json", "r", encoding="utf-8") as f:
    dev_dict = json.loads(f.read())
# with open("new_contributors.json", "r", encoding="utf-8") as f:
#     dev_dict = json.loads(f.read())

# find the chains and the transitive closure
chains = []
for pair in pairs:
    found = False
    for chain in chains:
        if pair[0] in chain:
            chain.add(pair[1])
            found = True
        elif pair[1] in chain:
            chain.add(pair[0])
            found = True
    if not found:
        chains.append(set(pair))


# merge the existing developers in the users
# converting sets to lists
for key in dev_dict:
    dev_dict[key]['devKeys'] = set(dev_dict[key]['devKeys'])

for chain in chains:
    chain = list(chain)
    item1 = chain[0]
    for item in chain[1:]:
        item1_info = dev_dict[item1]
        item_info = dev_dict[item]
        dev_dict[item1]['devKeys'] = dev_dict[item1]['devKeys'].union(item_info['devKeys'])
        if dev_dict[item1]['first_commit_date'] > item_info['first_commit_date']:
            dev_dict[item1]['first_commit_date'] = item_info['first_commit_date']
            dev_dict[item1]["first_six_months"] = item_info["first_six_months"]
            dev_dict[item1]["first_two_years"] = item_info["first_two_years"]

            # remove the old developer
        dev_dict.pop(item)



# converting sets to lists
for key in dev_dict:
    dev_dict[key]['devKeys'] = list(dev_dict[key]['devKeys'])

with open('1-Devs_Dictionary_post5.json', 'w') as f:
    json.dump(dev_dict, f, indent=4)

