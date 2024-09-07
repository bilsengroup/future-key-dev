import json
from copy import deepcopy

devs_code_smells = {}

with open("9-All_code_smells.json", "r") as json_file:
    All_Issue_data = json.load(json_file)

with open("8-devs_issues.json", "r") as json_file:
    devs = json.load(json_file)

new_keys = {"codesmells_first_threshold" : 0}
new_keys2 = {"codesmells_second_threshold" : 0}


for dev in devs.values():
    dev.update(deepcopy(new_keys))
    dev.update(deepcopy(new_keys2))






for issue in All_Issue_data:

    if issue['type'] == 'CODE_SMELL':
        key = issue["author"]
        for dev in devs:
            if dev == key:
                if issue['creationDate'] < devs[dev]['first_six_months'] and issue['creationDate'] >= devs[dev]['first_commit_date']:
                    devs[dev]['codesmells_first_threshold'] += 1
                if issue['creationDate'] <= devs[dev]['first_two_years'] and issue['creationDate'] >= devs[dev]['first_six_months']:
                    devs[dev]['codesmells_second_threshold'] += 1
                break
            elif key in devs[dev]['devKeys']:
                if issue['creationDate'] < devs[dev]['first_six_months'] and issue['creationDate'] >= devs[dev]['first_commit_date']:
                    devs[dev]['codesmells_first_threshold'] += 1
                if issue['creationDate'] <= devs[dev]['first_two_years'] and issue['creationDate'] >= devs[dev]['first_six_months']:
                    devs[dev]['codesmells_second_threshold'] += 1
                break

with open("10-result.json", "w") as json_file:
    json.dump(devs, json_file)

sum = 0
for dev in devs_code_smells:
    sum += devs_code_smells[dev]


print(sum)