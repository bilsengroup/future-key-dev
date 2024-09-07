import json
from copy import deepcopy

with open("7-issues_data/7-3-result_issue_Events.json", "r", encoding="utf-8") as f:
    Issue_Events = json.loads(f.read())

with open("7-issues_data/7-1-result_issue_Assignees.json", "r", encoding="utf-8") as f:
    Issue_Assignees = json.loads(f.read())

with open("7-issues_data/7-2-result_issue_comments_.json", "r", encoding="utf-8") as f:
    Issue_Comments = json.loads(f.read())

with open("6-devs-commits.json", "r", encoding="utf-8") as f:
    devs = json.loads(f.read())

new_keys = {"issues_first_threshold" : {'ReOpened': 0,'Comments': 0,'Assigned': 0,'Closed': 0}}
new_keys2 = {"issues_second_threshold" : {'ReOpened': 0,'Comments': 0,'Assigned': 0,'Closed': 0}}


for dev in devs.values():
    dev.update(deepcopy(new_keys))
    dev.update(deepcopy(new_keys2))

result = {}
for issue in Issue_Events['nodes']:
    events_of_issue = []
    for event in issue["timelineItems"]["nodes"]:
        if event:
            if event['actor'] is not None:
                events_of_issue.append({'event': event["__typename"], 'actor': event["actor"]["login"], 'createdAt': event["createdAt"]})
                if event["__typename"] == 'ClosedEvent':
                    for dev in devs:
                        if dev == event['actor']['login']:
                            if event['createdAt'] < devs[dev]['first_six_months'] and event['createdAt'] >= devs[dev]['first_commit_date']:
                                devs[dev]['issues_first_threshold']['Closed'] += 1
                            if event['createdAt'] <= devs[dev]['first_two_years'] and event['createdAt'] >= devs[dev]['first_six_months']:
                                devs[dev]['issues_second_threshold']['Closed'] += 1
                            break
                        elif event['actor']['login'] in devs[dev]['devKeys']:
                            if event['createdAt'] < devs[dev]['first_six_months'] and event['createdAt'] >= devs[dev]['first_commit_date']:
                                devs[dev]['issues_first_threshold']['Closed'] += 1
                            if event['createdAt'] <= devs[dev]['first_two_years'] and event['createdAt'] >= devs[dev]['first_six_months']:
                                devs[dev]['issues_second_threshold']['Closed'] += 1
                            break

    for i,event in enumerate(events_of_issue):
        if event['event'] == 'ClosedEvent':
            if i < len(events_of_issue)-1:
                for dev in devs:
                    if dev == event['actor']:
                        if event['createdAt'] < devs[dev]['first_six_months'] and event['createdAt'] >= devs[dev]['first_commit_date']:
                            devs[dev]['issues_first_threshold']['ReOpened'] += 1
                        if event['createdAt'] <= devs[dev]['first_two_years'] and event['createdAt'] >= devs[dev]['first_six_months']:
                            devs[dev]['issues_second_threshold']['ReOpened'] += 1
                        break
                    elif event['actor'] in devs[dev]['devKeys']:
                        if event['createdAt'] < devs[dev]['first_six_months'] and event['createdAt'] >= devs[dev]['first_commit_date']:
                            devs[dev]['issues_first_threshold']['ReOpened'] += 1
                        if event['createdAt'] <= devs[dev]['first_two_years'] and event['createdAt'] >= devs[dev]['first_six_months']:
                            devs[dev]['issues_second_threshold']['ReOpened'] += 1
                        break


for issue in Issue_Assignees['nodes']:
    if issue['assignees']['nodes']:
        for assignee in issue['assignees']['nodes']:
            for dev in devs:
                if dev == assignee['login']:
                    if issue['createdAt'] < devs[dev]['first_six_months'] and issue['createdAt'] >= devs[dev]['first_commit_date']:
                        devs[dev]['issues_first_threshold']['Assigned'] += 1
                    if issue['createdAt'] <= devs[dev]['first_two_years'] and issue['createdAt'] >= devs[dev]['first_six_months']:
                        devs[dev]['issues_second_threshold']['Assigned'] += 1
                    break
                elif assignee['login'] in devs[dev]['devKeys']:
                    if issue['createdAt'] < devs[dev]['first_six_months'] and issue['createdAt'] >= devs[dev]['first_commit_date']:
                        devs[dev]['issues_first_threshold']['Assigned'] += 1
                    if issue['createdAt'] <= devs[dev]['first_two_years'] and issue['createdAt'] >= devs[dev]['first_six_months']:
                        devs[dev]['issues_second_threshold']['Assigned'] += 1
                    break

for issue in Issue_Comments['nodes']:
    if issue['comments']['nodes']:
        for comment in issue['comments']['nodes']:
            if comment['author'] is not None:
                for dev in devs:
                    if dev == comment['author']['login']:
                        if comment['createdAt'] < devs[dev]['first_six_months'] and comment['createdAt'] >= devs[dev]['first_commit_date']:
                            devs[dev]['issues_first_threshold']['Comments'] += 1
                        if comment['createdAt'] <= devs[dev]['first_two_years'] and comment['createdAt'] >= devs[dev]['first_six_months']:
                            devs[dev]['issues_second_threshold']['Comments'] += 1
                        break
                    elif comment['author']['login'] in devs[dev]['devKeys']:
                        if comment['createdAt'] < devs[dev]['first_six_months'] and comment['createdAt'] >= devs[dev]['first_commit_date']:
                            devs[dev]['issues_first_threshold']['Comments'] += 1
                        if comment['createdAt'] <= devs[dev]['first_two_years'] and comment['createdAt'] >= devs[dev]['first_six_months']:
                            devs[dev]['issues_second_threshold']['Comments'] += 1
                        break



with open("8-devs_issues.json", "w") as f:
    json.dump(devs, f)