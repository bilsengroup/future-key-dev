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

with open("4-requested_reviewer.graphql", "r") as f:
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
if os.path.exists("pr_queries/result.json"):
    with open("pr_queries/result.json", "r", encoding="utf-8") as f:
        result = json.loads(f.read())
else:
    result = dict()
    result["nodes"] = list()

while True:

    formatted_query = query.replace("{cursor}", f'"{cursor}"' if cursor else "null")

    # Send a GET request to the GitHub API
    while True:
        try:
            response = requests.post(endpoint, headers=headers, json={"query": formatted_query})
            break
        except:
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
        with open("last_response.json", "w", encoding="utf-8") as f:
            f.write(response.text)
        last_data = json.loads(response.text)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        break

    for node in last_data["data"]["repository"]["pullRequests"]["nodes"]:
        result["nodes"].append(node)

    if last_data["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]:
        print(
            f"{last_data['data']['repository']['pullRequests']['pageInfo']['hasNextPage']} - Fetching page {last_data['data']['repository']['pullRequests']['pageInfo']['endCursor']}")
        cursor = last_data["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]
    else:
        print(f"Done! {last_data['data']['repository']['pullRequests']['pageInfo']['endCursor']}")
        break

with open("4-extracted_requested_reviewers.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(result, indent=4, sort_keys=False))



