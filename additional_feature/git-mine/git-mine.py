import json
import sys
import os
import argparse
from classes import GitRepo


def parse_args():
    """
    Parse command line arguments.

    Returns:
        Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="Git log analysis tool")
    parser.add_argument(
        "--path", "-p", type=str, required=True, help="Path to the git repository"
    )
    parser.add_argument(
        "--authors", "-a", type=str, required=True, help="Path to the authors file"
    )
    return parser.parse_args()


def main():
    """
    Main function to extract commits, analyze logs, and write stats to a file.
    """
    args = parse_args()

    if not os.path.isdir(args.path + "/.git"):
        print("Invalid git directory path.")
        sys.exit(1)

    repo_path = args.path

    with open(args.authors, "r") as file:
        author_merge_list = json.load(file)

    repo = GitRepo(repo_path)
    repo.extract_commits(author_merge_list)
    print("Done extracting commits.")
    developers, files = repo.analyze()

    print("Logs analyzed.")

    with open(f"{os.path.dirname(os.path.abspath(__file__))}/devs.csv", "w") as file:
        print("NAME,EMAIL,GH_USERNAME,LOC,DEAD_LOC,SURVIVAL_RATE", file=file)
        for dev in developers:
            print(dev, file=file)
        print(f"Written stats to {os.path.abspath(file.name)}")


if __name__ == "__main__":
    main()
