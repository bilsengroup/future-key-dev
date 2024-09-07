import json
from copy import deepcopy

with open('4-extracted_requested_reviewers.json', 'r') as f:
    prs = json.load(f)

with open('3-devs_prs.json', 'r') as f:
    devs = json.load(f)


new_key = {'requestedReviewer' : 0}


for dev in devs.values():
    dev["PR_reviews_first_threshold"].update(deepcopy(new_key))
    dev["PR_reviews_second_threshold"].update(deepcopy(new_key))

for pr in prs['nodes']:
    if len(pr['reviewRequests']['nodes']) > 0:
        for request in pr['reviewRequests']['nodes']:
            for dev in devs:
                try:
                    if dev == request['requestedReviewer']['login']:
                        if pr['createdAt'] < devs[dev]['first_six_months'] and pr['createdAt']>=devs[dev]['first_commit_date']:
                            devs[dev]['PR_reviews_first_threshold']['requestedReviewer'] += 1
                        if pr['createdAt'] <= devs[dev]['first_two_years'] and pr['createdAt'] >= devs[dev]['first_six_months']:
                            devs[dev]['PR_reviews_second_threshold']['requestedReviewer'] += 1
                        break
                    elif request['requestedReviewer']['login'] in devs[dev]['devKeys']:
                        if pr['createdAt'] < devs[dev]['first_six_months'] and pr['createdAt']>= devs[dev]['first_commit_date']:
                            devs[dev]['PR_reviews_first_threshold']['requestedReviewer'] += 1
                        if pr['createdAt'] <= devs[dev]['first_two_years'] and pr['createdAt'] >= devs[dev]['first_six_months']:
                            devs[dev]['PR_reviews_second_threshold']['requestedReviewer'] += 1
                        break
                except:
                    continue

with open('5-devs_prs2.json', 'w') as f:
    json.dump(devs, f, indent=4, sort_keys=True)
