# 10% of developers to be key developers
# first we preprocess the data and filter the 6 month limitation that should not exceed the current date

import json
from datetime import date
from dateutil import parser
from dateutil.relativedelta import relativedelta
from conf import *


def adjust_threshold(date):
    date_obj = parser.parse(date)
    # Add 6 months to the date
    date_obj_minus_6_months = date_obj + relativedelta(months=-6)
    # Convert back to string
    current_minus_six = date_obj_minus_6_months.isoformat()

    return current_minus_six




with open("13-result.json", "r") as json_file:
    data = json.load(json_file)

with open("ground_truth.json", "r") as json_file:
    ground_truth = json.load(json_file)






current_date = config_current_date
threshold_date = adjust_threshold(current_date)

# filter based on time and filter bots. In this scenario bots are considered those names which contain '[' in their names
new_devlist = {}
for dev in data:
    if data[dev]["first_six_months"] <= threshold_date and not('[' in dev or ']' in dev):
        new_devlist[dev] = data[dev]

a = len(new_devlist)

number_of_devs = len(new_devlist)
number_of_key_devs = number_of_devs // 10 #10 for precent
counter = 0

for key in new_devlist:
    new_devlist[key]['ground_truth'] = 0

for key in reversed(ground_truth):
    key = key[2]
    found = False
    for inner_key in reversed(new_devlist):
        devs_list = new_devlist[inner_key]['devKeys']
        # lower case all the elements in the list
        devs_list = [x.lower() for x in devs_list]
        if (key == inner_key) and counter < number_of_key_devs:
            if new_devlist[inner_key]['ground_truth'] == 1:
                print(f'innerkey: {inner_key}')
                print(f'gt: {key}')
            new_devlist[inner_key]['ground_truth'] = 1
            found = True
            counter += 1
            break
        elif (key.lower() in devs_list) and counter < number_of_key_devs:
            if new_devlist[inner_key]['ground_truth'] == 1:
                print(f'innerkey: {inner_key}')
                print(f'gt: {key}')
            new_devlist[inner_key]['ground_truth'] = 1
            found = True
            counter += 1
            break

    if not found:
        print(key)



print(len(data))
print(len(new_devlist))
with open("20-labeled_data.json", "w") as json_file:
    json.dump(new_devlist, json_file, indent=4)




def adjust_threshold(date):
    date_obj = parser.parse(date)
    # Add 6 months to the date
    date_obj_minus_6_months = date_obj + relativedelta(months=-6)
    # Convert back to string
    current_minus_six = date_obj_minus_6_months.isoformat()

    return current_minus_six
