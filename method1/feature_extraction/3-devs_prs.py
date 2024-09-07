import json
from copy import deepcopy


with open('1-Devs_Dictionary_post8_th.json', 'r') as f:
    devs = json.load(f)

with open('2-all_prs.json', 'r') as f:
    prs = json.load(f)

new_keys = {"PR_reviews_states_first_threshold" : {'APPROVED': 0, 'CHANGES_REQUESTED': 0, 'COMMENTED': 0, 'DISMISSED': 0, 'PENDING': 0}}
new_keys2 = {"PR_reviews_states_second_threshold" : {'APPROVED': 0, 'CHANGES_REQUESTED': 0, 'COMMENTED': 0, 'DISMISSED': 0, 'PENDING': 0}}
new_keys3 = {"PR_reviews_first_threshold" : {'number_of_changes_submitted': 0, 'number_of_pr_reviewed': 0, 'number_of_pr_review_comments': 0}}
new_keys4 = {"PR_reviews_second_threshold" : {'number_of_changes_submitted': 0, 'number_of_pr_reviewed': 0, 'number_of_pr_review_comments': 0}}


# for key, inner_dict in devs.items():
#     inner_dict.update(new_keys)

# for key, inner_dict in devs.items():
#     inner_dict.update(new_keys2)

# Loop through each inner dictionary and add new keys with value 0 if they don't exist

for dev in devs.values():
    dev.update(deepcopy(new_keys))

for dev in devs.values():
    dev.update(deepcopy(new_keys2))

for dev in devs.values():
    dev.update(deepcopy(new_keys3))

for dev in devs.values():
    dev.update(deepcopy(new_keys4))


for pr in prs['nodes']:
    for review in pr['reviews']['nodes']:
        if review['author'] is None:
            continue
        key = review['author']['login']
        if key is None:
            continue
        for dev in devs:
            if dev == key:
                if review['createdAt'] < devs[dev]['first_six_months'] and review['createdAt']>= devs[dev]['first_commit_date']:
                    devs[dev]['PR_reviews_states_first_threshold'][review['state']] += 1
                if review['createdAt'] <= devs[dev]['first_two_years'] and review['createdAt'] >= devs[dev]['first_six_months']:
                    devs[dev]['PR_reviews_states_second_threshold'][review['state']] += 1
                break
            elif key in devs[dev]['devKeys']:
                if review['createdAt'] < devs[dev]['first_six_months'] and review['createdAt']>=devs[dev]['first_commit_date']:
                    devs[dev]['PR_reviews_states_first_threshold'][review['state']] += 1
                if review['createdAt'] <= devs[dev]['first_two_years'] and review['createdAt'] >= devs[dev]['first_six_months']:
                    devs[dev]['PR_reviews_states_second_threshold'][review['state']] += 1
                break

for dev in devs:
    devs[dev]['PR_reviews_first_threshold']['number_of_changes_submitted'] = devs[dev]['PR_reviews_states_first_threshold']['CHANGES_REQUESTED']
    devs[dev]['PR_reviews_first_threshold']['number_of_pr_reviewed'] = devs[dev]['PR_reviews_states_first_threshold']['APPROVED'] + devs[dev]['PR_reviews_states_first_threshold']['DISMISSED'] + devs[dev]['PR_reviews_states_first_threshold']['CHANGES_REQUESTED'] + devs[dev]['PR_reviews_states_first_threshold']['COMMENTED'] + devs[dev]['PR_reviews_states_first_threshold']['PENDING']
    devs[dev]['PR_reviews_first_threshold']['number_of_pr_review_comments'] = devs[dev]['PR_reviews_states_first_threshold']['COMMENTED']
    devs[dev]['PR_reviews_second_threshold']['number_of_changes_submitted'] = devs[dev]['PR_reviews_states_second_threshold']['CHANGES_REQUESTED']
    devs[dev]['PR_reviews_second_threshold']['number_of_pr_reviewed'] = devs[dev]['PR_reviews_states_second_threshold']['APPROVED'] + devs[dev]['PR_reviews_states_second_threshold']['DISMISSED'] + devs[dev]['PR_reviews_states_second_threshold']['CHANGES_REQUESTED'] + devs[dev]['PR_reviews_states_second_threshold']['COMMENTED'] + devs[dev]['PR_reviews_states_second_threshold']['PENDING']
    devs[dev]['PR_reviews_second_threshold']['number_of_pr_review_comments'] = devs[dev]['PR_reviews_states_second_threshold']['COMMENTED']


with open('3-devs_prs.json', 'w') as f:
    json.dump(devs, f)

