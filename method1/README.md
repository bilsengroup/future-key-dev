# Project Configuration Instructions

## Initial Setup
Initially, we need to modify the `conf.py` file. The following parameters should be set:

1. **config_access_token**: Insert your GitHub token. This token is needed to fetch data from GitHub.
2. **config_tokens**: If possible, it would be better to provide more tokens. This is useful, especially in the case of larger repositories where one token reaches the limit for fetching the data. In this case, the next token in the list will be used.
3. **config_repo_owner**: Repository owner.
4. **config_repo_name**: Repository name.
5. **config_first_release_date_str**: You can obtain it from the repository's GitHub page. The value should be a date.
6. **config_current_date**: Set to today's date.
7. **config_api_token**: It is the token that SonarQube gives for the project.
8. **config_componentKeys**: Project's key (identifier) in SonarQube.

## Determining First Commit Date for Developers
The first commit date of the developers whose first commit dates are before the initial release date of the project is set to their first commit date after the initial release date. Again, those developers whose first commit date falls after the initial release date remain unchanged.

## Data Extraction
The first thing we need in the code is the raw data to be extracted. First of all, run the following files to extract the needed raw data:
1. `0-developer_extraction.py`: Extracts all commits of the repository and outputs `0-AllCommits.json`. In this file, the commit date, author's full name, email, and login name can be found.
2. `2-extract_PRs.py`
3. `4-extract_PRs_requested_reviews.py`
4. `7-1-extract_issue_assignees.py`
5. `7-2-extract_issue_comments.py`
6. `7-3-extract_issue_events.py`
7. `9-extract_codesmells.py`: Before running this file, we should scan the project using Sonar Scanner.

## Post Data Extraction Processing
After extracting the raw data using GitHub API, the following scripts should now be run:
1. `1-DevsInitialization_1.py`: This script yields a dictionary of contributors. The keys of this dictionary (`dev_dict`) are the usernames (login) of the contributors, and the values are dictionaries. The keys of the inner dictionaries are name, email, first_commit_date, first_six_month, and dev_keys. Dev_keys is a set for each contributor that stores all identifiers (logins, names, emails) for each contributor.
2. `1-DevsInitialization_1_Postprocess_2.py`: In `1-Devs_Dictionary_1.json` we observe some users that their keys are email addresses. In order to obtain their corresponding user (login), we query (from GitHub API) their full name and emails, respectively.
3. `1-DevsInitialization_1_Postprocess_3.py`: In the `1-to_be_removed_to_be_added.json` file, if the new key is inside the `dev_dict`'s keys merge it with the corresponding user with the email and then delete the email key from the `dev_dict`.
4. Additional scripts up to `1-DevsInitialization_1_Postprocess_7_then.py` detail further processing steps, including merging contributor data and refining contributor dictionaries based on similarity and manual checks.

## Specific to Gitea and Moby Projects
Details the specific scripts and processing steps for the Gitea and Moby projects, such as `Maintainers_Gitea.py` and `Maintainers_Moby.py`.

## Evaluation Steps
After obtaining the dataset, place it in the `xlsx_files` directory and configure the necessary parameters in `data_analysis/config.py`. Specific to RQ3, decide whether to apply PCA for additional features obtained from method2. Then, run `KNN.py`, `LR.py`, `Naïve_Bayes.py`, and `Random_Forest.py` to get the results.
