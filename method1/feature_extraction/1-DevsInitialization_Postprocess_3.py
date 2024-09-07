import json
from dateutil import parser
from dateutil.relativedelta import relativedelta
from conf import *
import requests
import time


with open("1-Devs_Dictionary_post_2.json", "r", encoding="utf-8") as f:
    dev_dict = json.loads(f.read())

with open("1-to_be_removed_to_be_added.json", "r", encoding="utf-8") as f:
    to_be_removed_to_be_added = json.loads(f.read())


# converting sets to lists
for key in dev_dict:
    dev_dict[key]['devKeys'] = set(dev_dict[key]['devKeys'])
counter = 0


# for i,(old1,new1) in enumerate(to_be_removed_to_be_added):
#     for j,(old2,new2) in enumerate(to_be_removed_to_be_added):
#         if old1 == old2 and i != j:
#             print(old1)
#         if old1 == new2 and i != j:
#             print(old1)
#         if new1 == old2 and i != j:
#             print(new1)
#         if new1 == new2 and i != j:
#             print(new1)

# merge the existing developers in the users
for old,new in to_be_removed_to_be_added:
    if new in dev_dict:
        new_info = dev_dict[new]
        old_info = dev_dict[old]
        dev_dict[new]['devKeys'] = dev_dict[new]['devKeys'].union(old_info['devKeys'])
        if dev_dict[new]['first_commit_date'] > old_info['first_commit_date']:
            dev_dict[new]['first_commit_date'] = old_info['first_commit_date']
            dev_dict[new]["first_six_months"] = old_info["first_six_months"]
            dev_dict[new]["first_two_years"] = old_info["first_two_years"]

        # remove the old developer
        dev_dict.pop(old)
    else:
        dev_dict[new] = dev_dict[old]
        dev_dict.pop(old)


# converting sets to lists
for key in dev_dict:
    dev_dict[key]['devKeys'] = list(dev_dict[key]['devKeys'])
with open('1-Devs_Dictionary_post3.json', 'w') as f:
    json.dump(dev_dict, f, indent=4)
print(len(dev_dict))


