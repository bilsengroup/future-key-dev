import requests
import base64
import pandas as pd

# Configuration
repo_owner = 'go-gitea'
repo_name = 'gitea'
file_path = 'MAINTAINERS'
github_token = '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'  # Replace with your GitHub token

# Setup for GitHub API
headers = {'Authorization': f'token {github_token}'}
base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}'

def get_maintainers_by_year(year):
    # Get commits for the file within the year
    until_date = f'{year}-01-01T23:59:59Z'
    since_date = f'{year-1}-01-01T00:00:01Z'
    commits_url = f'{base_url}/commits?path={file_path}&until={until_date}&since={since_date}'
    commits_response = requests.get(commits_url, headers=headers)
    commits = commits_response.json()

    if not commits:
        return []

    # Get the last commit of the year
    last_commit = commits[0]
    last_commit_sha = last_commit['sha']

    # Get the commit details to access the tree
    commit_details_url = f'{base_url}/git/commits/{last_commit_sha}'
    commit_details_response = requests.get(commit_details_url, headers=headers)
    commit_details = commit_details_response.json()

    # Access the tree from the commit
    tree_sha = commit_details['tree']['sha']
    tree_url = f'{base_url}/git/trees/{tree_sha}'
    tree_response = requests.get(tree_url, headers=headers)
    tree = tree_response.json()

    # Find the blob SHA for the MAINTAINERS file
    for file in tree['tree']:
        if file['path'] == file_path:
            file_blob_sha = file['sha']
            break
    else:
        return []

    # Get the file content from the blob SHA
    file_url = f'{base_url}/git/blobs/{file_blob_sha}'
    file_response = requests.get(file_url, headers=headers)
    file_content = file_response.json()

    # Decode the base64 content
    if 'content' in file_content:
        decoded_content = base64.b64decode(file_content['content']).decode('utf-8')
        return decoded_content.splitlines()  # Return a list of maintainers
    else:
        return []

# Iteratively get and print maintainers from a range of years
start_year = 2022
end_year = 2024
all_maintainers = set()

for year in range(start_year, end_year + 1):
    maintainers = get_maintainers_by_year(year)
    all_maintainers.update(maintainers)
    print(f'Maintainers in {year}: {maintainers}')
    print(f'Number of maintainers in {year}: {len(maintainers)}')

# Final list of unique maintainers
text_final_maintainers_list = list(all_maintainers)
final_maintainers_list = []
for line in text_final_maintainers_list:
    if "(" in line:
        tba = line[line.find("(")+2:line.find(")")]
        if tba != "":
          final_maintainers_list.append(tba)

print(f'Total unique maintainers from {start_year} to {end_year}:{final_maintainers_list}')
print(f"Total unique maintainers from {start_year} to {end_year}: {len(final_maintainers_list)}")

#save to csv
pd.DataFrame(final_maintainers_list).to_csv(f'gitea-maint-{start_year}-{end_year}.csv', index=False)

import json
#with open(f'gitea_maintaner-{start_year}-{end_year}.json', 'w') as f:
#    json.dump(list(all_maintainers), f)
# Save the DataFrame to an Excel file
# df = pd.DataFrame(final_maintainers_list, columns=['Maintainers'])
# excel_path = 'Maintainers_List.xlsx'
# df.to_excel(excel_path, index=False)
# print(f'Maintainers list saved to {excel_path}')
