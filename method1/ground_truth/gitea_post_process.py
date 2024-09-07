import json


#open a json file
with open('..\\feature_extraction\\1-Devs_Dictionary_post7.json', 'r') as json_file:
    dev_dict = json.load(json_file)

# Load the JSON data from the file
file_path = 'gitea_maintaner.json'
with open(file_path, 'r') as file:
    contributors = json.load(file)

# Function to parse the contributor strings and create the desired dictionary
def parse_contributors(contributors):
    parsed_data = []
    for contributor in contributors:
        name_part, email_part, username_part = contributor.split(" <", 1)[0], contributor.split(" <", 1)[1].split(">")[0], contributor.split(" (@")[1][:-1]
        full_name = name_part.strip()
        email = email_part.strip()
        username = username_part.strip()
        parsed_data.append([full_name, email, username])
    return parsed_data

# Parse the contributors
parsed_contributors = parse_contributors(contributors)

#dump to json file
with open('gitea_maintaner_parsed.json', 'w') as f:
    json.dump(parsed_contributors, f, indent=4)

for key in dev_dict:
    dev_dict[key]['devKeys'] = set(dev_dict[key]['devKeys'])



for candidate_dev_list in parsed_contributors:
    found = False
    new_set = set(candidate_dev_list)
    for key in dev_dict:
        for item in dev_dict[key]['devKeys']:
            if item in new_set:
                dev_dict[key]['devKeys'] = dev_dict[key]['devKeys'].union(new_set)
                counter += 1
                found = True
                break
        if found:
            break
    if not found:
        print(candidate_dev_list)



for key in dev_dict:
    dev_dict[key]['devKeys'] = list(dev_dict[key]['devKeys'])
with open('new_contributors.json', 'w') as f:
    json.dump(dev_dict, f, indent=4)






