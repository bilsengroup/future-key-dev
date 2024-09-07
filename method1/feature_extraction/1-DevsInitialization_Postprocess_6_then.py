# IMPORTANT
#this script should be run after extracting all prs and issues (after 2,4,7)


import json
from fuzzywuzzy import fuzz
import numpy as np
import re

with open("1-Devs_Dictionary_post5.json", "r") as json_file:
    data = json.load(json_file)

with open("7-issues_data/7-3-result_issue_Events.json", "r", encoding="utf-8") as f:
    Issue_Events = json.loads(f.read())

with open("7-issues_data/7-1-result_issue_Assignees.json", "r", encoding="utf-8") as f:
    Issue_Assignees = json.loads(f.read())

with open("7-issues_data/7-2-result_issue_comments_.json", "r", encoding="utf-8") as f:
    Issue_Comments = json.loads(f.read())

with open('2-all_prs.json', 'r') as f:
    prs = json.load(f)


all_names = []
for issue in Issue_Events['nodes']:
    events_of_issue = []
    for event in issue["timelineItems"]["nodes"]:
        if event:
            if event['actor'] is not None:
                all_names.append(event["actor"]["login"])


for issue in Issue_Assignees['nodes']:
    if issue['assignees']['nodes']:
        for assignee in issue['assignees']['nodes']:
            all_names.append(assignee['login'])

for issue in Issue_Comments['nodes']:
    if issue['author'] is not None:
        all_names.append(issue['author']['login'])

for pr in prs['nodes']:
    for review in pr['reviews']['nodes']:
        if review['author'] is None:
            continue
        key = review['author']['login']
        if key is None:
            continue
        all_names.append(key)


print(len(all_names))
counter = 0
scounter = 0
all_names = set(all_names)
all_new_names = set()
for key in all_names:
    found = False
    for inner_key in data:
        if key in data[inner_key]['devKeys']:
            counter += 1
            found = True
            break
    if not found:
        scounter += 1
        all_new_names.add(key)

print(counter)
print(scounter)
print(len(set(all_names)))







def preprocess_string(s):
    # Remove '@' and everything after it
    s = re.sub(r'@.*', '', s)
    # Convert to lowercase
    s = s.lower()

    s = s.replace('github', '')
    return s
def calculate_pairwise_similarity(list1, list2):
    # Create an empty matrix to store similarity scores
    similarity_matrix = np.zeros((len(list1), len(list2)))

    # Calculate pairwise similarity scores
    for i, item1 in enumerate(list1):
        for j, item2 in enumerate(list2):
            if item1 == '' and item2 == '':
                a = 0

            similarity_matrix[i, j] = fuzz.ratio(item1, item2)
            a = 1

    # Return the maximum similarity score for each item in list1
    max_similarities = similarity_matrix.max(axis=1)

    # get max of max_similarities
    max_max_similarities = max(max_similarities)
    # Calculate the overall similarity as the mean of maximum similarities
    overall_similarity = np.mean(max_similarities)

    return max_max_similarities, overall_similarity
# convert dictionary to list
pairs = []
all_new = [[key] for key in all_new_names]
for list1 in all_new:
    for dev in data:
        list2 = data[dev]["devKeys"]
        list2 = [preprocess_string(s) for s in list2]
        # exclude string if it is ''
        list2 = [s for s in list2 if s != '']
        similarity_score , overall_sim = calculate_pairwise_similarity(list1,list2)
        if similarity_score > 90 and overall_sim > 80:
            pairs.append((list1[0], dev))
            print(f"Similarity score between {list1[0]} and {dev}: {similarity_score:.2f}, {overall_sim:.2f}")


with open('1-Devs_pairs_6.json', 'w') as f:
    json.dump(pairs, f, indent=4)

