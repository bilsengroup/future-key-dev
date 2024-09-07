import json
from dateutil import parser
from dateutil.relativedelta import relativedelta
from conf import *
import requests
import time


with open("1-Devs_Dictionary_1.json", "r", encoding="utf-8") as f:
    dev_dict = json.loads(f.read())

temp_token = config_access_token
list_of_tokens = config_tokens
def change_token():
    global temp_token
    global list_of_tokens
    print(f"Changing token: current token is {temp_token}")
    temp_token = config_tokens.pop()
    print(f"New token is {temp_token}")
    time.sleep(1)
    #insert the temp_token to the end of the list
    list_of_tokens.insert(0,temp_token)
def get_github_user_by_email(email):
    # GitHub API endpoint to search for users
    url = f"https://api.github.com/search/users?q={email}+in:email"
    flag = True
    while flag == True:
        # Set up the headers with the access token for authentication
        headers = {
            "Authorization": f"token {config_access_token}"
        }

        # Make the request to the GitHub API
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            flag = False
            data = response.json()
            # Check if there are any users found
            if data['total_count'] > 0:
                # Return the login name of the first user found
                users = [(user['login']) for user in data['items']]
                for user in users:
                    if user is not None:
                        return user
                return None
            else:
                return None
        else:
            print(f"Error occured in emails request, {email}")
            change_token()




def get_github_user_by_name(full_name):
    # GitHub API endpoint to search for users
    url = f"https://api.github.com/search/users?q={full_name}+in:fullname"
    flag = True
    while flag == True:
        # Set up the headers with the access token for authentication
        headers = {
            "Authorization": f"token {temp_token}"
        }
        # time.sleep(1)
        # Make the request to the GitHub API
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Check if there are any users found
            if data['total_count'] > 0:
                # Return a list of user logins and their corresponding names
                users = [(user['login']) for user in data['items']]
                for item in data['items']:
                    if item['url'] is not None:
                        inner_flag = True
                        while inner_flag==True:
                            time.sleep(1)
                            headers = {"Authorization": f"token {temp_token}"}
                            second_response = requests.get(item['url'], headers=headers)
                            if second_response.status_code == 200:
                                data = second_response.json()
                                inner_flag = False
                                if data['name'] == full_name:
                                    return data['login']
                            else:
                                print(f"Error occured in second request, {full_name}")
                                change_token()
                return None
            else:
                return None
        else:
            print(f"Error occured in first request, {full_name}")
            change_token()

def sort_keys(keys):
    sorted_keys = []
    for key in keys:
        if ' ' in key:
            sorted_keys.append(key)
    for key in keys:
        if ' ' not in key:
            sorted_keys.append(key)
    return sorted_keys





# converting sets to lists
for key in dev_dict:
    dev_dict[key]['devKeys'] = set(dev_dict[key]['devKeys'])

request_count = 0
first_count = 0
to_be_removed_to_be_added = []

for key in dev_dict:
    if '@' in key:
        first_count += 1
        print(first_count)
        sorted_keys = sort_keys(dev_dict[key]['devKeys'])
        for devKey in sorted_keys:
            if '@' in devKey:
                request_count += 1
                found_user = get_github_user_by_email(devKey)
                if found_user is not None:
                    dev_dict[key]['devKeys'].add(found_user)
                    t = (key,found_user)
                    to_be_removed_to_be_added.append(t)
                    break
            elif ' ' in devKey:
                request_count += 1
                found_user = get_github_user_by_name(devKey)
                if found_user is not None:
                    dev_dict[key]['devKeys'].add(found_user)
                    t = (key,found_user)
                    to_be_removed_to_be_added.append(t)
                    break






# converting sets to lists
for key in dev_dict:
    dev_dict[key]['devKeys'] = list(dev_dict[key]['devKeys'])
with open('1-Devs_Dictionary_post_2.json', 'w') as f:
    json.dump(dev_dict, f, indent=4)

with open('1-to_be_removed_to_be_added.json', 'w') as f:
    json.dump(to_be_removed_to_be_added, f, indent=4)



