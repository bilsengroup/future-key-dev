import json
import requests
from conf import *

repo_owner = config_repo_owner
repo_name = config_repo_name

access_token = config_access_token

# Get the list of contributors for the repository
headers = {'Authorization': f'token {access_token}'}

url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/stats/contributors'
key_devs = []

response = requests.get(url, headers=headers, params={ 'per_page': 500})

result = response.json()

for contributor in result:
    key_devs.append(contributor['author']['login'])


with open(f"ground_truth.json", 'w') as json_file:
    json.dump(key_devs, json_file)