import requests
import base64
import toml
import pandas as pd
import json
# Configuration
repo_owner = 'moby'
repo_name = 'moby'
file_path = 'MAINTAINERS'
github_token = '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'  # Replace with your GitHub token

# Setup for GitHub API
headers = {'Authorization': f'token {github_token}'}
base_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}'

def get_core_maintainers_by_year(year):
    until_date = f'{year}-12-31T23:59:59Z'
    since_date = f'{year-1}-01-01T00:00:01Z'
    commits_url = f'{base_url}/commits?path={file_path}&until={until_date}&since={since_date}'
    commits_response = requests.get(commits_url, headers=headers)
    commits = commits_response.json()

    if not commits:
        return set()  # Return an empty set if no commits

    last_commit = commits[0]
    last_commit_sha = last_commit['sha']

    commit_details_url = f'{base_url}/git/commits/{last_commit_sha}'
    commit_details_response = requests.get(commit_details_url, headers=headers)
    commit_details = commit_details_response.json()

    tree_sha = commit_details['tree']['sha']
    tree_url = f'{base_url}/git/trees/{tree_sha}'
    tree_response = requests.get(tree_url, headers=headers)
    tree = tree_response.json()

    for file in tree['tree']:
        if file['path'] == file_path:
            file_blob_sha = file['sha']
            break
    else:
        return set()  # Return an empty set if file not found

    file_url = f'{base_url}/git/blobs/{file_blob_sha}'
    file_response = requests.get(file_url, headers=headers)
    file_content = file_response.json()

    if 'content' in file_content:
        decoded_content = base64.b64decode(file_content['content']).decode('utf-8')
        toml_data = toml.loads(decoded_content)
        core_maintainers = set(toml_data['Org']['Core maintainers']['people'])
        curators = set(toml_data['Org']['Curators']['people'])
        return core_maintainers.union(curators)  # Return the union of both sets
    else:
        return set()  # Return an empty set if content not available

# Iteratively get and print core maintainers from a range of years
start_year = 2018  # Start year
end_year = 2021  # End year
all_core_maintainers = set()

for year in range(start_year, end_year + 1):
    yearly_maintainers = get_core_maintainers_by_year(year)
    all_core_maintainers.update(yearly_maintainers)  # Update the global set to include this year's maintainers
    print(f'Core maintainers and curators in {year}: {yearly_maintainers}')
    print(f'Core maintainers and curators in {year}: {len(yearly_maintainers)}')
print(f'All core maintainers and curators cross years: {all_core_maintainers}')
print(f'All core maintainers and curators cross years: {len(all_core_maintainers)}')

# write all_core_maintainers to json file
all_core_maintainers = list(all_core_maintainers)
#save to csv
pd.DataFrame(all_core_maintainers).to_csv(f'moby_m_c-{start_year}-{end_year}.csv', index=False)

#with open(f'moby_m_c-{start_year}-{end_year}.json', 'w') as f:
#    json.dump(list(all_core_maintainers), f)

# Convert the set of all maintainers to a pandas DataFrame
df_maintainers = pd.DataFrame(list(all_core_maintainers), columns=['Core Maintainers and Curators'])

# # Save the DataFrame to an Excel file
# excel_filename = 'Core_Maintainers_and_Curators_Moby.xlsx'
# df_maintainers.to_excel(excel_filename, index=False)
#
# print(f'The list of unique core maintainers and curators has been saved to {excel_filename}.')
