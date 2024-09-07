import requests
import os
import json
from dotenv import load_dotenv
from conf import *

load_dotenv()

# Replace these with your GitHub username and personal access token
username = config_username

tokens = config_tokens
access_token = config_access_token

with open("7-issues_data/query_Issue_Events.graphql", "r") as f:
    query = f.read()

# Specify the repository and API endpoint
repo_owner = config_repo_owner
repo_name = config_repo_name
query = query.replace("{repo_owner}", f'"{repo_owner}"')
query = query.replace("{repo_name}", f'"{repo_name}"')

endpoint = f"https://api.github.com/graphql"

# Set up the headers with your access token
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

cursor = None

if os.path.exists("issue_queries/result.json"):
    with open("issue_queries/result.json", "r", encoding="utf-8") as f:
        result = json.loads(f.read())
else:
    result = dict()
    result["nodes"] = list()

PageCount = 1

while True:

    formatted_query = query.replace("{cursor}", f'"{cursor}"' if cursor else "null")

    # Send a GET request to the GitHub API
    while True:
        try:
            response = requests.post(endpoint, headers=headers, json={"query": formatted_query})
            break
        except:
            with open("result_temp_issue_Events.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(result, indent=4, sort_keys=False))
            print(f"Timeout - Cursor: {cursor}\nRetrying...")
            access_token = tokens.pop(0)
            tokens.append(access_token)
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            continue

    # Check the status code of the response
    if response.status_code == 200:
        # The request was successful; parse and print the response data
        with open("7-issues_data/last_response.json", "w", encoding="utf-8") as f:
            f.write(response.text)
        last_data = json.loads(response.text)
    else:
        with open("7-issues_data/result_temp_issue_Events.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(result, indent=4, sort_keys=False))
        print(f"Error: {response.status_code} - {response.text}")
        access_token = tokens.pop(0)
        tokens.append(access_token)
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        continue

    for node in last_data["data"]["repository"]["issues"]["nodes"]:
        result["nodes"].append(node)

    if last_data["data"]["repository"]["issues"]["pageInfo"]["hasNextPage"]:
        print(
            f"{last_data['data']['repository']['issues']['pageInfo']['hasNextPage']} - Fetching page {last_data['data']['repository']['issues']['pageInfo']['endCursor']} - {PageCount}")
        PageCount += 1
        cursor = last_data["data"]["repository"]["issues"]["pageInfo"]["endCursor"]
    else:
        print(f"Done! {last_data['data']['repository']['issues']['pageInfo']['endCursor']}")
        break

with open("7-issues_data/7-3-result_issue_Events.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(result, indent=4, sort_keys=False))



