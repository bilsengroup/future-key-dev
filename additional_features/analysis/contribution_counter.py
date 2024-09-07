import json

def create_author():
    author = {}
    author["commits"] = {}
    author["commits"]["number of commits"] = 0
    author["commits"]["number of additions"] = 0
    author["commits"]["number of deletions"] = 0
    author["commits"]["number of changed files"] = 0
    author["issues"] = {}
    author["issues"]["number of issues"] = 0
    author["issues"]["number of issue comments taken"] = 0
    author["issues"]["number of issue comments made"] = 0
    author["issues"]["number of issue assignments"] = 0
    author["issues"]["peers commented to this author"] = []
    author["issues"]["number of peers commented"] = 0
    author["issues"]["peers this author commented to"] = []
    author["issues"]["number of peers commented to"] = 0
    author["pull requests"] = {}
    author["pull requests"]["number of pull requests opened"] = 0
    author["pull requests"]["number of pull request comments made"] = 0
    author["pull requests"]["number of pull request comments taken"] = 0
    author["pull requests"]["number of pull request assignments"] = 0
    author["pull requests"]["reviews"] = {}
    author["pull requests"]["reviews"]["number of pull request reviews"] = 0
    author["pull requests"]["reviews"]["number of approved prs"] = 0
    author["pull requests"]["reviews"]["number of changes requested prs"] = 0
    author["pull requests"]["reviews"]["number of commented prs"] = 0
    author["pull requests"]["reviews"]["number of dismissed prs"] = 0
    author["pull requests"]["reviews"]["number of pending reviews"] = 0

    return author

# Read the JSON file
with open('./gh_api_queries/commit_queries/result.json') as file:
    commit_data = json.load(file)
with open('./gh_api_queries/issue_queries/result.json') as file:
    issue_data = json.load(file)
with open('./gh_api_queries/pr_queries/result.json') as file:
    pull_request_data = json.load(file)

# Create a dictionary to store the contribution counts
contributions = {}

# Iterate over the entries in the loaded dictionary
for node in commit_data["nodes"]:
    # Extract the author's name
    author = node["author"]["user"]["login"] if node["author"]["user"] else node["author"]["email"]
    # Increment the contribution count for the author
    if author not in contributions:
        contributions[author] = create_author()

    contributions[author]["commits"]["number of commits"] = contributions[author]["commits"].get("number of commits", 0) + 1
    contributions[author]["commits"]["number of additions"] = contributions[author]["commits"].get("number of additions", 0) + node["additions"]
    contributions[author]["commits"]["number of deletions"] = contributions[author]["commits"].get("number of deletions", 0) + node["deletions"]
    contributions[author]["commits"]["number of changed files"] = contributions[author]["commits"].get("number of changed files", 0) + node["changedFiles"]

for node in issue_data["nodes"]:
    # Extract the author's name
    author = node["author"]["login"] if node["author"] else "null"
    # Increment the contribution count for the author
    if author not in contributions:
        contributions[author] = create_author()
    contributions[author]["issues"]["number of issues"] = contributions[author]["issues"].get("number of issues", 0) + 1
    contributions[author]["issues"]["number of issue comments taken"] = contributions[author]["issues"].get("number of issue comments taken", 0) + len(node["comments"]["nodes"])

    for comment in node["comments"]["nodes"]:
        comment_author = comment["author"]["login"] if comment["author"] else "null"
        if comment_author not in contributions:
            contributions[comment_author] = create_author()
        contributions[comment_author]["issues"]["number of issue comments made"] = contributions[comment_author]["issues"].get("number of issue comments made", 0) + 1

        if comment_author not in contributions[author]["issues"]["peers commented to this author"]:
            contributions[author]["issues"]["peers commented to this author"].append(comment_author)
            contributions[author]["issues"]["number of peers commented"] = contributions[author]["issues"].get("number of peers commented", 0) + 1

        if author not in contributions[comment_author]["issues"]["peers this author commented to"]:
            contributions[comment_author]["issues"]["peers this author commented to"].append(author)
            contributions[comment_author]["issues"]["number of peers commented to"] = contributions[comment_author]["issues"].get("number of peers commented to", 0) + 1

    for assignee in node["assignees"]["nodes"]:
        author = assignee["login"]
        if author not in contributions:
            contributions[author] = create_author()
        contributions[author]["issues"]["number of issue assignments"] = contributions[author]["issues"].get("number of issue assignments", 0) + 1

for node in pull_request_data["nodes"]:
    # Extract the author's name
    author = node["author"]["login"] if node["author"] else "null"
    # Increment the contribution count for the author
    if author not in contributions:
        contributions[author] = create_author()
    contributions[author]["pull requests"]["number of pull requests opened"] = contributions[author]["pull requests"].get("number of pull requests opened", 0) + 1
    contributions[author]["pull requests"]["number of pull request comments taken"] = contributions[author]["pull requests"].get("number of pull request comments taken", 0) + len(node["comments"]["nodes"])

    for comment in node["comments"]["nodes"]:
        author = comment["author"]["login"] if comment["author"] else "null"
        if author not in contributions:
            contributions[author] = create_author()
        
        contributions[author]["pull requests"]["number of pull request comments made"] = contributions[author]["pull requests"].get("number of pull request comments made", 0) + 1

    review_authors = []
    for review in node["reviews"]["nodes"]:
        author = review["author"]["login"] if review["author"] else "null"
        review_authors.append(author)

        if author not in contributions:
            contributions[author] = create_author()
        contributions[author]["pull requests"]["reviews"]["number of pull request reviews"] = contributions[author]["pull requests"]["reviews"].get("number of pull request reviews", 0) + 1
        if review["state"] == "APPROVED":
            contributions[author]["pull requests"]["reviews"]["number of approved prs"] = contributions[author]["pull requests"]["reviews"].get("number of approved prs", 0) + 1
        elif review["state"] == "CHANGES_REQUESTED":
            contributions[author]["pull requests"]["reviews"]["number of changes requested prs"] = contributions[author]["pull requests"]["reviews"].get("number of changes requested prs", 0) + 1
        elif review["state"] == "COMMENTED":
            contributions[author]["pull requests"]["reviews"]["number of commented prs"] = contributions[author]["pull requests"]["reviews"].get("number of commented prs", 0) + 1
        elif review["state"] == "DISMISSED":
            contributions[author]["pull requests"]["reviews"]["number of dismissed prs"] = contributions[author]["pull requests"]["reviews"].get("number of dismissed prs", 0) + 1
        elif review["state"] == "PENDING":
            contributions[author]["pull requests"]["reviews"]["number of pending reviews"] = contributions[author]["pull requests"]["reviews"].get("number of pending reviews", 0) + 1

    for assignee in node["assignees"]["nodes"]:
        author = assignee["login"]
        if author not in contributions:
            contributions[author] = create_author()
        contributions[author]["pull requests"]["number of pull request assignments"] = contributions[author]["pull requests"].get("number of pull request assignments", 0) + 1

        if author not in review_authors:
            contributions[author]["pull requests"]["reviews"]["number of pending reviews"] = contributions[author]["pull requests"]["reviews"].get("number of pending reviews", 0) + 1


for contributor in contributions:
    contributions[contributor]["total contributions"] = (
        contributions[contributor]["commits"]["number of commits"]
        + contributions[contributor]["issues"]["number of issues"]
        + contributions[contributor]["pull requests"]["number of pull requests opened"]
    )

sorted_contributions = sorted(contributions.items(), key=lambda x: x[1]["total contributions"], reverse=True)

# Print the contribution counts for each author
with open('./analysis/contribution_counts.json', 'w') as file:
    json.dump(sorted_contributions, file, indent=4, sort_keys=True)
