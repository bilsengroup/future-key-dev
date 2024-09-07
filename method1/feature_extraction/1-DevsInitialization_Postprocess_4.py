from fuzzywuzzy import fuzz
import numpy as np
import json
import re
# open json file
with open('1-Devs_Dictionary_post3.json', 'r') as f:
    devs = json.load(f)
# with open('new_contributors.json', 'r') as f:
#     devs = json.load(f)


def preprocess_string(s):
    # Remove '@' and everything after it
    s = re.sub(r'@.*', '', s)
    # Convert to lowercase
    s = s.lower()

    s = s.replace('github', '')
    return s
def calculate_pairwise_similarity(list1, list2):
    # Create an empty matrix to store similarity scores
    similarity_matrix = np.zeros((len(list1), len(list2)))

    # Calculate pairwise similarity scores
    for i, item1 in enumerate(list1):
        for j, item2 in enumerate(list2):
            # if item1 == '' and item2 == '':
            #     a = 0

            similarity_matrix[i, j] = fuzz.ratio(item1, item2)
            # a = 1

    # Return the maximum similarity score for each item in list1
    max_similarities = similarity_matrix.max(axis=1)

    # get max of max_similarities
    max_max_similarities = max(max_similarities)
    # Calculate the overall similarity as the mean of maximum similarities
    overall_similarity = np.mean(max_similarities)

    return max_max_similarities, overall_similarity
# convert dictionary to list
devs_list = list(devs)
pairs = []
for i in range(len(devs_list)):
    list1 = devs[devs_list[i]]["devKeys"]
    list1 = [preprocess_string(s) for s in list1]
    # exclude string if it is ''
    list1 = [s for s in list1 if s != '']
    for j in range(i+1, len(devs_list)):
        list2 = devs[devs_list[j]]["devKeys"]
        list2 = [preprocess_string(s) for s in list2]
        # exclude string if it is ''
        list2 = [s for s in list2 if s != '']
        similarity_score , overall_sim = calculate_pairwise_similarity(list1,list2)
        if similarity_score > 90 and overall_sim > 80:
            pairs.append((devs_list[i], devs_list[j]))
            print(f"Similarity score between {devs_list[i]} and {devs_list[j]}: {similarity_score:.2f}, {overall_sim:.2f}")


with open('1-Devs_Pairs_similars.json', 'w') as f:
    json.dump(pairs, f, indent=4)


