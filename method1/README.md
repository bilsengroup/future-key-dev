# Project Configuration Instructions

## Initial Configuration
Initially, we need to modify the `conf.py` file. The following parameters should be set:
1. `config_access_token`: Insert your GitHub token. This token is needed to fetch data from GitHub.
2. `config_tokens`: If possible, it would be better to provide more tokens. This is useful, especially in the case of larger repositories where one token reaches the limit for fetching the data. In this case the next token in the list will be used.
3. `config_repo_owner`: Repository owner
4. `config_repo_name`: Repository name
5. `config_first_release_data_str`: You can obtain it from the repository's GitHub page. The value should be a date.
6. `config_current_data`: Set to today's date.
7. `config_api_token`: It is the token that SonarQube gives for the project.
8. `config_componentKeys`: Project's key (identifier) in the SonarQube.

## Determining First Commit Date
How do we determine the first commit date for developers?
The first commit date of the developers whose first commit dates are before the initial release date of the project is set to their first commit date after the initial release date. Again, those developers whose first commit date falls after the initial release date remain unchanged.

## Data Extraction
The first thing we need in the code is the raw data to be extracted. First of all, run the following files to extract the needed raw data:
1. `0-developer_extraction.py`: Extracts all commits of the repository and outputs `0-AllCommits.json`. In this file, the commit date, author's full name, email, and login name can be found.
2. `2-extract_PRs.py`
3. `4-extract_Prs_requested_reviews.py`
4. `7-1-extract_issue_assinees.py`
5. `7-2-extract_issue_comments.py`
6. `7-3-extract_issue_events.py`
7. `9-extract_codesmells.py`: Before running this file, we should scan the project using Sonar Scanner.

## Post Data Extraction Scripts
After extracting the raw data using GitHub API, the following scripts should now be run:
1. `1-DevsInitialization_1.py`: This script yields a dictionary of contributors. The keys of this dictionary (`dev_dict`) are the usernames (login) of the contributors, and the values are dictionaries. The keys of the inner dictionaries are name, email, first_commit_date, first_six_month, and dev_keys. Dev_keys is a set for each contributor that stores all identifiers (logins, names, emails) for each contributor. To obtain the contributors to the project, we iterate over the commits (`0-AllCommits.json`). In each iteration, we create a sample consisting of the username, email, and full name of the commit's author. Then, using the `find_similar()` function, we determine if the sample has an exact match of its elements with all contributors' dev_keys. If yes, the function will return the corresponding developer's key. Then, the contributor's keys will be added to the `dev_dict` set of the contributors found. The output of this script is `1-Devs_Dictionary_1.json`.
2. `1-DevsInitialization_1_Postprocess_2.py`: In `1-Devs_Dictionary_1.json` we observe some users that their keys are email addresses. In order to obtain their corresponding user (login), we query (from GitHub API) their full name and emails, respectively. The output of this step is `1-Devs_Dictionary_Post_2.json` and `1-to_be_removed_to_be_added.json` (Which indicates that the contributor with the email key will be deleted and the corresponding contributor with login key will be added to the `dev_dict`).
3. `1-DevsInitialization_1_Postprocess_3.py`: In the `1-to_be_removed_to_be_added.json` file, if the new key is inside the `dev_dict`'s keys merge it with the corresponding user with the email and then delete the email key from the `dev_dict`. If the new key is not inside the `dev_dict`, just create a new entity, place the key with the email's info on it, and then delete the user with the email. The output of this step is `1-Devs_Dictionary_post3.json`.
4. `1-DevsInitialization_1_Postprocess_4.py`: This script is for finding the similarities between the different contributors' dev_keys. We should adjust thresholds for the similarities (similarity_score and overall_sim). The similar keys are stored in `1-Devs_Pairs_similars.json`. Then, we should manually check the pairs to make sure they really match.
5. `1-DevsInitialization_1_Postprocess_5.py`: In this file, we find chains in the pairs to see if there is a transitive relation. After finding the chains, we merge them. The output is `1-Devs_Dictionary_post5.json`.
6. `1-DevsInitialization_1_Postprocess_6_then.py`: In this script, we collect all names that appeared in all issues and PRs (comments, assignee, etc). Then we check to see which names do not have an exact match in at least one contributor's dev_keys, and we label them as all_new_names. Now, we run the similarity function on each of these names and all contributors' dev_keys. If the similarity exceeds a certain threshold, we consider it a candidate match and store it in `1-Devs_pairs_6.json`.
7. `1-DevsInitialization_1_Postprocess_7_then.py`: After finding the candidate matches, we check them manually. The same as before. We find the chains and merge. The output is `1-Devs_Dictionary_post7.json`.

## Specific to Gitea and Moby Projects
Specific to Gitea project (steps 8-9):
8. `Ground_truth/Manitaners_Gitea.py`: Running this script will output the ground truth that the repository itself suggests.
9. `Ground_truth/gitea_post_process.py`: This file preprocesses the ground truth data and gets the full name, email, and login for each contributor in the list. Then, it adds the keys to the contributors' dev_keys. After that, we need to repeat `1-DevsInitialization_1_Postprocess_4` and `1-DevsInitialization_1_Postprocess_5`, and if new similarities between the contributors appear, we detect them and merge them.
Specific to Moby project (step 10):
10. `Ground_truth/Maintainers_Moby.py`: Running this script will output the ground truth that the repository itself suggests.
11. `3-devs_prs.py`: The PRs and features related to PRs are counted for each developer.
12. `5-requested_reviewer.py`: How many times a developer is requested as a reviewer is counted.
13. `6-devs-commits.py`: Counts the number of commits, additions, deletions, and changed files.
14. `8-devs_issues.py`: Counts the features related to issues (assignees, comments, reopens) for each developer.
15. `10-devs_code_smell.py`: Counts the number of code_smells a developer has in the project.

## Specific to RQ3 (steps 16-17):
16. `11-add_code_survival.py`: After obtaining the `code_survival_feature.csv` from additional_features, you should add the file to the root and then run this script to merge the new feature with the previously calculated features.
17. `13-merged.py`: After obtaining the `combined_embedings.csv` from method2, you should add the file to the root and then run the script to merge the new features with the previous ones.

## Additional Steps
18. `extract_GitHub_insights_devs`: mine ground truth data from GitHub Insights.
19. `20-add_labels_v2.py`: Labels the data. We should specify what percentage of the ground truth data to be used. Also, the source for the Ground Truth data should be specified in this script. The "first commit date threshold" is applied in this file.
20. `Z_generate_excel`: This script will generate the final dataset of the repository.

## Evaluation Steps
After obtaining the dataset, you should place it in the `xlsx_files` directory. Then, in the `data_analysis/config.py` The following parameters should be configured:
1. `root_name`: The reports will be generated with this name.
2. `excel_file`: Specifies the dataset to be used in the model.

## Specific to RQ3
3. `apply_pca`: It is a flag indicating whether or not to use PCA for 600 additional features (obtained from the method2) in the dataset.
After configuration, Run the `KNN.py`, `LR.py`, `Naïve_Bayes.py`, and `Random_Forest.py` to get the results.

