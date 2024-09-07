import requests
import json
import time
from conf import *

# endDate = "2020-10-01T00:00:00+0000"

url = 'https://api.github.com/graphql'

tokens = config_tokens
access_token = config_access_token

headers = {
    'Authorization': f'Bearer {access_token}'
}

query = """
query($repo_owner: String!, $repo_name: String!, $cursor: String) { 
  repository(owner: $repo_owner, name: $repo_name) {
    defaultBranchRef {
      target {
        ... on Commit {
          history(first: 100, after: $cursor) {
            nodes {
              oid
              committedDate
              author {
                name
                email
                date
                user {
                  login
                }
              }
              additions
              deletions
              changedFiles
            }
            pageInfo {
              hasNextPage
              endCursor
            }
          }
        }
      }
    }
  }
}
"""
repo_owner = config_repo_owner
repo_name = config_repo_name

cursor = None
All_commits = []
request_count = 1
while True:
    variables = {
        'repo_owner': repo_owner,
        'repo_name': repo_name,
        'cursor': cursor
    }
    try:
        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    except:
        print("Error in request ... Changing Token!")
        access_token = tokens.pop(0)
        tokens.append(access_token)
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        time.sleep(10)
        continue



    if response.status_code == 200:
        data = response.json()
        commit_edges = data['data']['repository']['defaultBranchRef']['target']['history']['nodes']
        All_commits.extend(commit_edges)


        hasNextPage = data['data']['repository']['defaultBranchRef']['target']['history']['pageInfo']['hasNextPage']
        if request_count % 10 == 0:
            with open('0-AllCommits_temp.json', 'w') as f:
                json.dump(All_commits, f)
            print("Sleeping for 10 seconds")

        if hasNextPage:
            cursor = data['data']['repository']['defaultBranchRef']['target']['history']['pageInfo']['endCursor']
            print(f"Request #{request_count} - hasNextPage: {hasNextPage} - Cursor: {cursor}")
        else:
            break
        request_count += 1
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        break


with open('0-AllCommits.json', 'w') as f:
    json.dump(All_commits, f)