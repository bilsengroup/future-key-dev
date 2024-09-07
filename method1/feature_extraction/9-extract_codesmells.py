import requests
from urllib.parse import urljoin
import json
from conf import *

sonarqube_url = "http://localhost:9000"
api_endpoint = "/api/issues/search"
api_token = config_api_token

headers = {
    "Authorization": f"Bearer {api_token}" if api_token else None,
}

component_key = config_componentKeys
params = {
    "componentKeys": component_key,
    "types": "CODE_SMELL",
    "ps": 500,  # Set the page size to 100, or adjust as needed
    "p": 1,
    # "branch": "",
    # Add other parameters as needed
}

url = urljoin(sonarqube_url, api_endpoint)
All_Issue_data = []
while True:

    response = requests.get(url, headers=headers, params=params)
    print("Request URL:", response.url)  # Print the final URL for debugging

    if response.status_code == 200:
        issues_data = response.json()
        issues_list = issues_data.get("issues", [])

        if issues_list:
            All_Issue_data.extend(issues_list)
            params["p"] += 1  # Move to the next page
        else:
            break  # No more issues, exit the loop
    else:
        print(f"Error: {response.status_code} - {response.text}")
        break

print("Total issues:", len(All_Issue_data))
with open("9-All_code_smells.json", "w") as json_file:
    json.dump(All_Issue_data, json_file)