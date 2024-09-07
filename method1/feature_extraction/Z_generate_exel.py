import pandas as pd
import json
from datetime import datetime


# Load JSON data into a DataFrame
with open("20-labeled_data.json", "r") as json_file:
    json_data = json.load(json_file)
print(len(json_data))

def convert_date(datetime_str):
    # Your datetime string
    datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")
    return datetime_obj.strftime("%Y-%m-%d")

    return date_part


new_dict = {}
for key in json_data:
    inner_dict ={
        '6m_resolved_issues': json_data[key]['issues_first_threshold']['Closed'],
        '6m_assigned_issues': json_data[key]['issues_first_threshold']['Assigned'],
        '6m_bug_reopened': json_data[key]['issues_first_threshold']['ReOpened'],
        '6m_issue_comment': json_data[key]['issues_first_threshold']['Comments'],
        '6m_LOC': json_data[key]['commits_first_threshold']['total_additions'] + json_data[key]['commits_first_threshold']['total_deletions'],
        '6m_change_reviews': json_data[key]['PR_reviews_first_threshold']['number_of_changes_submitted'],
        '6m_as_requested_reviewer': json_data[key]['PR_reviews_first_threshold']['requestedReviewer'],
        '6m_reviewed_prs': json_data[key]['PR_reviews_first_threshold']['number_of_pr_reviewed'],
        '6m_pr_review_comments': json_data[key]['PR_reviews_first_threshold']['number_of_pr_review_comments'],
        '6m_code_smells': json_data[key]['codesmells_first_threshold'],
        '6m_total_commits': json_data[key]['commits_first_threshold']['total_commits'],
        '6m_total_files': json_data[key]['commits_first_threshold']['total_changed_files'],
        'SURVIVAL_RATE': json_data[key]['SURVIVAL_RATE']
    }
    if 'additional_features' in json_data[key].keys():
        for k in json_data[key]['additional_features']:
            inner_dict[k] = json_data[key]['additional_features'][k]
    inner_dict['ground_truth'] = json_data[key]['ground_truth']
    new_dict[key] = inner_dict





with open("Z_result.json", "w") as json_file:
    json.dump(new_dict, json_file)

flat_data = [{"key": key, **value} for key, value in new_dict.items()]

df = pd.DataFrame(flat_data)


# Rename the 'index' column to a more meaningful name (e.g., 'keys')

# Write DataFrame to Excel file
excel_file_path = "gitea_dataset.xlsx"
df.to_excel(excel_file_path, index=False)

print(f"Data has been written to {excel_file_path}")