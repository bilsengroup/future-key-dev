import json
from copy import deepcopy

with open('0-AllCommits.json', 'r') as f:
    all_commits = json.load(f)

with open('5-devs_prs2.json', 'r') as f:
    devs = json.load(f)


new_keys = {"commits_first_threshold" : {'total_commits': 0, 'total_additions': 0, 'total_deletions': 0, 'total_changed_files': 0}}
new_keys2 = {"commits_second_threshold" : {'total_commits': 0, 'total_additions': 0, 'total_deletions': 0, 'total_changed_files': 0}}


for dev in devs.values():
    dev.update(deepcopy(new_keys))
    dev.update(deepcopy(new_keys2))

for commit in all_commits:
    new_sample = (commit['author']['user']['login'] if commit['author']['user'] is not None else None, commit['author']['email'],commit['author']['name'])
    key = None
    if commit['author']['user'] is not None:
        key = commit['author']['user']['login']
    elif commit['author']['email'] is not None:
        key = commit['author']['email']
    elif commit['author']['name'] is not None:
        key = commit['author']['name']
    else:
        continue
    for dev in devs:
        if new_sample[0] is not None and new_sample[0] == dev:
            if commit['committedDate'] < devs[dev]['first_six_months'] and commit['committedDate'] >= devs[dev]['first_commit_date']:
                devs[dev]['commits_first_threshold']['total_commits'] += 1
                devs[dev]['commits_first_threshold']['total_additions'] += commit['additions']
                devs[dev]['commits_first_threshold']['total_deletions'] += commit['deletions']
                devs[dev]['commits_first_threshold']['total_changed_files'] += commit['changedFiles']
            if commit['committedDate'] <= devs[dev]['first_two_years'] and commit['committedDate'] >= devs[dev]['first_six_months']:
                devs[dev]['commits_second_threshold']['total_commits'] += 1
                devs[dev]['commits_second_threshold']['total_additions'] += commit['additions']
                devs[dev]['commits_second_threshold']['total_deletions'] += commit['deletions']
                devs[dev]['commits_second_threshold']['total_changed_files'] += commit['changedFiles']
            break
        elif new_sample[1] in devs[dev]['devKeys'] or new_sample[2] in devs[dev]['devKeys']:
            if commit['committedDate'] < devs[dev]['first_six_months'] and commit['committedDate'] >= devs[dev]['first_commit_date']:
                devs[dev]['commits_first_threshold']['total_commits'] += 1
                devs[dev]['commits_first_threshold']['total_additions'] += commit['additions']
                devs[dev]['commits_first_threshold']['total_deletions'] += commit['deletions']
                devs[dev]['commits_first_threshold']['total_changed_files'] += commit['changedFiles']
            if commit['committedDate'] <= devs[dev]['first_two_years'] and commit['committedDate'] >= devs[dev]['first_six_months']:
                devs[dev]['commits_second_threshold']['total_commits'] += 1
                devs[dev]['commits_second_threshold']['total_additions'] += commit['additions']
                devs[dev]['commits_second_threshold']['total_deletions'] += commit['deletions']
                devs[dev]['commits_second_threshold']['total_changed_files'] += commit['changedFiles']
            break

with open('6-devs-commits.json', 'w') as f:
    json.dump(devs, f)
