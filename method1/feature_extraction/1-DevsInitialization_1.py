import json
from dateutil import parser
from dateutil.relativedelta import relativedelta
from conf import *

def calculate_dates(date):
    date_obj = parser.parse(date)
    # Add 6 months to the date
    date_obj_plus_6_months = date_obj + relativedelta(months=+6)
    # Convert back to string
    first_six_months = date_obj_plus_6_months.isoformat()
    # date_obj = parser.parse(first_six_months)
    # Add 2 years to the date
    date_obj_plus_2_years = date_obj + relativedelta(years=+2)
    # Convert back to string
    first_two_years = date_obj_plus_2_years.isoformat()
    return first_six_months, first_two_years

first_release_date_str = config_first_release_date_str
# first_release_date = parser.parse(first_release_date_str)


with open("0-AllCommits.json", "r", encoding="utf-8") as f:
    all_commits = json.loads(f.read())

#iterated reverse
dev_dict = {}


def find_similar(sample):
    for simKey in dev_dict:
        if (sample[0] in dev_dict[simKey]["devKeys"] and sample[0] is not None) or sample[1] in dev_dict[simKey]["devKeys"] or sample[2] in dev_dict[simKey]["devKeys"]:
            # for sampleKey in sample:
            #     if sampleKey is not None:
            #         dev_dict[simKey]["devKeys"].add(sampleKey)
            return simKey
    return None


def add_sample(sample, found_key):
    for key in sample:
        if key is not None:
            dev_dict[found_key]['devKeys'].add(key)


count = 0
for commit in reversed(all_commits):
    new_sample = (commit['author']['user']['login'] if commit['author']['user'] is not None else None, commit['author']['email'], commit['author']['name'])
    found_sample = find_similar(new_sample)

    key = None
    if found_sample is None:
        if commit['author']['user'] is not None:
            key = commit['author']['user']['login']
        elif commit['author']['email'] is not None:
            key = commit['author']['email']
        elif commit['author']['name'] is not None:
            key = commit['author']['name']
        else:
            continue

    # new_sample = [commit['author']['user']['login'] if commit['author']['user'] is not None else None, commit['author']['email'], commit['author']['name']]
    # key = check_sample(new_sample)
    # print(key)
    a = commit['committedDate']

    commit_date = parser.parse(commit['committedDate'])

    if found_sample is None:
        if first_release_date_str is not None and MODE == 1:
            commit_date_dev = commit['committedDate'] if commit['committedDate'] > first_release_date_str else first_release_date_str
        elif first_release_date_str is None and MODE == 1:
            commit_date_dev = commit['committedDate']
        elif first_release_date_str is not None and MODE == 2:
            commit_date_dev = commit['committedDate'] if commit['committedDate'] > first_release_date_str else first_release_date_str

        first_six_months, first_two_years = calculate_dates(commit_date_dev)
        #initializing the contributor with the following information.
        dev_dict[key] = {'name': commit['author']['name'],'email': commit['author']['email'],'first_commit_date': commit_date_dev,'first_six_months':first_six_months, 'first_two_years':first_two_years,'devKeys': set(),'MODE_2_flag': True}
        # adding the new sample elements to the key's devKeys in dev_dict
        add_sample(new_sample, key)

    elif found_sample is not None :
        # dev_dict[key]['first_commit_date'] = commit['committedDate']
        if first_release_date_str is not None and MODE == 1:
            commit_date_dev = commit['committedDate'] if commit['committedDate'] > first_release_date_str else first_release_date_str
        elif first_release_date_str is None and MODE == 1:
            commit_date_dev = commit['committedDate']
        if MODE == 1:
            if dev_dict[found_sample]['first_commit_date'] > commit_date_dev:
                dev_dict[found_sample]['first_commit_date'] = commit_date_dev
                first_six_months, first_two_years = calculate_dates(commit_date_dev)
                dev_dict[found_sample]['first_six_months'] = first_six_months
                dev_dict[found_sample]['first_two_years'] = first_two_years


        if first_release_date_str is not None and MODE == 2:
            if commit['committedDate'] > first_release_date_str:
                commit_date_dev = commit['committedDate']
                if dev_dict[found_sample]['first_commit_date'] > first_release_date_str:
                    dev_dict[found_sample]['MODE_2_flag'] = False
                if dev_dict[found_sample]['MODE_2_flag']:
                    dev_dict[found_sample]['first_commit_date'] = commit_date_dev
                    dev_dict[found_sample]['MODE_2_flag'] = False
                if commit_date_dev > first_release_date_str and commit_date_dev < dev_dict[found_sample]['first_commit_date'] and not dev_dict[found_sample]['MODE_2_flag']:
                    dev_dict[found_sample]['first_commit_date'] = commit_date_dev
                first_six_months, first_two_years = calculate_dates(dev_dict[found_sample]['first_commit_date'])
                dev_dict[found_sample]['first_six_months'] = first_six_months
                dev_dict[found_sample]['first_two_years'] = first_two_years



        add_sample(new_sample, found_sample)


# converting sets to lists
for key in dev_dict:
    dev_dict[key]['devKeys'] = list(dev_dict[key]['devKeys'])

with open('1-Devs_Dictionary_1.json', 'w') as f:
    json.dump(dev_dict, f, indent=4)

