from datetime import datetime
import pytz
import os
import subprocess
from tqdm import tqdm
from dateutil.relativedelta import relativedelta

MONTHS = 6


class Author:
    """
    Represents an author with their name, email, GitHub username, lines of code (loc),
    dead lines of code (dead_loc), survival rate, first commit date, and aliases.
    """

    def __init__(self, name, email):
        self.name: str = name
        self.email: str = email
        self.gh_username: str = ""
        self.loc: int = 0
        self.dead_loc: int = 0
        self.survival_rate: float = 0.0
        self.first_commit_date: datetime = None
        self.aliases = []

    def __str__(self):
        return f"{self.name},{self.email},{self.gh_username},{self.loc},{self.dead_loc},{self.survival_rate}"


class GitCommit:
    """
    Represents a Git commit.

    Attributes:
        commit_hash (str): The hash of the commit.
        is_initial_commit (bool): Indicates if the commit is the initial commit.
        author (Author): The author of the commit.
        date (datetime): The date and time of the commit.
        diffs (list): The list of diffs (changes) in the commit.
        repo (str): The path to the repository.

    Methods:
        extract_commits_from_git_log(cls, path_to_repo, before="", after=""): Extracts commits from the Git log.
        set_diffs(self): Sets the diffs for the commit.
        __str__(self): Returns a string representation of the commit.
    """

    def __init__(
        self,
        commit_hash,
        author,
        date: str,
        repo: str,
        diffs=[],
        is_initial_commit=False,
    ):
        self.commit_hash: str = commit_hash
        self.is_initial_commit: bool = is_initial_commit
        self.author: Author = author
        self.date: datetime = datetime.strptime(date, "%Y-%m-%d %H:%M:%S %z")
        self.diffs: list = diffs
        self.repo: str = repo

    @classmethod
    def extract_commits_from_git_log(
        cls, path_to_repo: str, before: str = "", after: str = ""
    ) -> list:
        """
        Extracts commits from the Git log.

        Args:
            path_to_repo (str): The path to the Git repository.
            before (str, optional): The date and time before which to extract commits. Defaults to "".
            after (str, optional): The date and time after which to extract commits. Defaults to "".

        Returns:
            list: The list of extracted commits.

        Raises:
            Exception: If there is an error extracting commits from the Git log.
        """
        between = ""
        if before != "":
            between += f"--before={before} "
        if after != "":
            between += f"--after={after}"

        absolute_path = os.path.abspath(path_to_repo)
        os.chdir(absolute_path)
        if between != "":
            command = f"git log --reverse --pretty=format:%H%n%an%n%ae%n%ad%n### --date=iso {between}"
        else:
            command = (
                "git log --reverse --pretty=format:%H%n%an%n%ae%n%ad%n### --date=iso"
            )
        result = subprocess.run(command.split(), capture_output=True)
        if result.returncode != 0:
            raise Exception(result.stderr.decode("utf-8"))

        commits = []
        for i, commit in enumerate(result.stdout.decode("utf-8").split("\n###\n")):
            lines = commit.split("\n")
            if len(lines) < 4:
                print(f"Error: {lines}")
                continue

            commit_hash = lines[0]
            author = Author(lines[1], lines[2])
            date = lines[3]

            if i == 0:
                commits.append(
                    cls(
                        commit_hash, author, date, absolute_path, is_initial_commit=True
                    )
                )
            else:
                commits.append(cls(commit_hash, author, date, absolute_path))

        print(f"{len(commits)} commits extracted")

        return commits

    def set_diffs(self):
        """
        Sets the diffs for the commit.

        Raises:
            Exception: If there is an error getting the diffs.
        """
        os.chdir(self.repo)
        if self.is_initial_commit:
            show_result = subprocess.run(
                ["git", "show", "-U0", self.commit_hash], capture_output=True
            )
            if show_result.returncode != 0:
                raise Exception(show_result.stderr.decode("utf-8"))

            result = subprocess.run(
                ["tail", "-n", "+7"], capture_output=True, input=show_result.stdout
            )
        else:
            result = subprocess.run(
                ["git", "diff", "-U0", f"{self.commit_hash}^", self.commit_hash],
                capture_output=True,
            )
            if result.returncode != 0:
                result = subprocess.run(
                    ["git", "show", "-U0", self.commit_hash], capture_output=True
                )
                if result.returncode != 0:
                    raise Exception(result.stderr.decode("utf-8"))

                result = subprocess.run(
                    ["tail", "-n", "+7"], capture_output=True, input=result.stdout
                )

                if result.returncode != 0:
                    raise Exception(result.stderr.decode("utf-8"))

        diffs = []
        try:
            for diff in result.stdout.decode("utf-8").split("diff --git"):
                if diff == "":
                    continue

                diff_chunks = diff.split("\n@@")
                diff_head = diff_chunks[0]
                diff_head_lines = diff_head.split("\n")
                filename = diff_head_lines[0].split("b/")[-1]
                old_filename = None
                try:
                    if diff_head_lines[1].startswith("similarity index"):
                        old_filename = diff_head_lines[2].split(" ")[-1]
                        if diff_head_lines[1].split(" ")[-1] == "100%":
                            diffs.append(GitDiff(filename, [], old_filename))
                            continue
                except IndexError:
                    print(f"Error: {diff_head_lines}")

                lines = []
                for chunk in diff_chunks[1:]:
                    for line in chunk.split("\n")[1:]:
                        if (
                            line == ""
                            or line == "+"
                            or line == "-"
                            or line.endswith("\\ No newline at end of file")
                        ):
                            continue
                        lines.append(GitLine(line, self.author))

                diffs.append(GitDiff(filename, lines, old_filename))

        except UnicodeDecodeError as e:
            print(f"Error: {e}")

        self.diffs = diffs

    def __str__(self):
        return f"{self.commit_hash} {self.author.name} {self.date} {self.diffs} {self.repo}"


class GitFile:
    """
    Represents a file in a Git repository.

    Attributes:
        name (str): The name of the file.
        lines (list[GitLine]): The lines of code in the file.
    """

    def __init__(self, name, lines):
        self.name: str = name
        self.lines: list[GitLine] = lines

    def __str__(self):
        return f"{self.name} {self.lines}"


class GitLine:
    """
    Represents a line of code in a Git repository.

    Attributes:
        operation (str): The operation performed on the line ('+' for addition, '-' for modification).
        content (str): The content of the line.
        author (Author): The author of the line.

    Methods:
        __str__: Returns a string representation of the GitLine object.
    """

    def __init__(self, line, author):
        self.operation: str = line[0]
        self.content: str = line[1:]
        self.author: Author = author

    def __str__(self):
        return f"{self.operation}\n{self.content}\n{self.author}"


class GitDiff:
    """
    Represents a Git diff for a specific file.

    Attributes:
        filename (str): The name of the file.
        lines (list[GitLine]): The list of GitLine objects representing the changes in the file.
        old_filename (str, optional): The old name of the file in case of a rename.
    """

    def __init__(self, filename, lines, old_filename=None):
        self.filename: str = filename
        self.lines: list[GitLine] = lines
        self.old_filename = old_filename  # For renames

    def __str__(self):
        return f"{self.filename} {self.lines} {self.old_filename}"


class SquashedGitCommit(GitCommit):
    """
    Represents a squashed git commit.

    Inherits from the GitCommit class and adds an end_commit_hash attribute to represent the end commit hash
    of the squashed commit.

    Attributes:
        commit_hash (str): The commit hash of the squashed commit.
        author (str): The author of the squashed commit.
        date (str): The date of the squashed commit.
        repo (str): The repository of the squashed commit.
        diffs (list[GitDiff]): The list of GitDiff objects representing the differences in the squashed commit.
        is_initial_commit (bool): Indicates whether the squashed commit is the initial commit.
        end_commit_hash (str): The end commit hash of the squashed commit.

    Methods:
        from_commit(cls, commit: GitCommit, squashed_commit_hash: str) -> SquashedGitCommit:
            Creates a SquashedGitCommit object from a GitCommit object and a squashed commit hash.
        squash_consequent_commits(commits: list[GitCommit]) -> list[GitCommit]:
            Squashes consequent commits with the same author into a single SquashedGitCommit object.
        set_diffs(self):
            Sets the diffs attribute of the SquashedGitCommit object by executing git commands.
    """

    def __init__(
        self,
        commit_hash,
        author,
        date: str,
        repo: str,
        diffs,
        is_initial_commit,
        end_commit_hash,
    ):
        super().__init__(commit_hash, author, date, repo, diffs, is_initial_commit)
        self.end_commit_hash: str = end_commit_hash

    @classmethod
    def from_commit(cls, commit: GitCommit, squashed_commit_hash: str):
        """
        Create a new instance of the class using information from a GitCommit object.

        Args:
            commit (GitCommit): The GitCommit object containing the commit information.
            squashed_commit_hash (str): The hash of the squashed commit.

        Returns:
            An instance of the class initialized with the commit information.

        """
        return cls(
            commit.commit_hash,
            commit.author,
            commit.date.strftime("%Y-%m-%d %H:%M:%S %z"),
            commit.repo,
            commit.diffs,
            commit.is_initial_commit,
            squashed_commit_hash,
        )

    @staticmethod
    def squash_consequent_commits(commits: list[GitCommit]) -> list[GitCommit]:
        """
        Squashes consequent commits with the same author.

        Args:
            commits (list[GitCommit]): A list of GitCommit objects representing the commits to be squashed.

        Returns:
            list[GitCommit]: A list of GitCommit objects representing the squashed commits.

        """
        squashed_commits = []
        squashed_commit = None
        for commit in commits:
            # Never squash initial commit
            if commit.is_initial_commit:
                squashed_commits.append(commit)
                continue

            if squashed_commit is None:
                squashed_commit = commit
                continue

            if squashed_commit.author.name == commit.author.name:
                if not isinstance(squashed_commit, SquashedGitCommit):
                    squashed_commit = SquashedGitCommit.from_commit(
                        squashed_commit, commit.commit_hash
                    )
                else:
                    squashed_commit.end_commit_hash = commit.commit_hash
            else:
                squashed_commits.append(squashed_commit)
                squashed_commit = commit

        if squashed_commit is not None:
            squashed_commits.append(squashed_commit)

        print(f"Squashed {len(commits)} commits into {len(squashed_commits)} commits")
        return squashed_commits

    def set_diffs(self):
        """
        Sets the diffs attribute of the GitRepo object by retrieving the differences between commits.

        Raises:
            Exception: If there is an error executing the Git commands.
        """
        os.chdir(self.repo)
        if self.is_initial_commit:
            show_result = subprocess.run(
                ["git", "show", "-U0", self.commit_hash], capture_output=True
            )
            if show_result.returncode != 0:
                raise Exception(show_result.stderr.decode("utf-8"))

            result = subprocess.run(
                ["tail", "-n", "+7"], capture_output=True, input=show_result.stdout
            )
        else:
            result = subprocess.run(
                ["git", "diff", "-U0", f"{self.commit_hash}^", self.end_commit_hash],
                capture_output=True,
            )
            if result.returncode != 0:
                result = subprocess.run(
                    ["git", "show", "-U0", self.commit_hash], capture_output=True
                )
                if result.returncode != 0:
                    raise Exception(result.stderr.decode("utf-8"))

        diffs = []
        try:
            for diff in result.stdout.decode("utf-8").split("diff --git"):
                if diff == "":
                    continue

                diff_chunks = diff.split("\n@@")
                diff_head = diff_chunks[0]
                diff_head_lines = diff_head.split("\n")
                filename = diff_head_lines[0].split("b/")[-1]
                old_filename = None
                try:
                    if diff_head_lines[1].startswith("similarity index"):
                        old_filename = diff_head_lines[2].split(" ")[-1]
                        if diff_head_lines[1].split(" ")[-1] == "100%":
                            diffs.append(GitDiff(filename, [], old_filename))
                            continue
                except IndexError:
                    print(f"Error: {diff_head_lines}")

                lines = []
                for chunk in diff_chunks[1:]:
                    for line in chunk.split("\n")[1:]:
                        if (
                            line == ""
                            or line == "+"
                            or line == "-"
                            or line.endswith("\\ No newline at end of file")
                        ):
                            continue
                        lines.append(GitLine(line, self.author))

                diffs.append(GitDiff(filename, lines, old_filename))

        except UnicodeDecodeError as e:
            print(f"Error: {e}")

        self.diffs = diffs


class GitRepo:
    """
    Represents a Git repository.

    Attributes:
        path (str): The path to the repository.
        commits (list[GitCommit]): The list of Git commits in the repository.
        authors (list[Author]): The list of authors contributing to the repository.
        files (list[GitFile]): The list of files in the repository.

    Methods:
        extract_commits(author_merge_dict, before="", after=""): Extracts commits from the Git log and sets the commits, authors, and files attributes.
        analyze(): Analyzes the logs of the commits in the repository and calculates survival rates for authors.

    """

    def __init__(self, path_to_repo: str):
        self.path: str = path_to_repo
        self.commits: list[GitCommit] = []
        self.authors: list[Author] = []
        self.files: list[GitFile] = []

    def extract_commits(self, author_merge_dict, before: str = "", after: str = ""):
        """
        Extracts commits from the Git log and sets the commits, authors, and files attributes.

        Args:
            author_merge_dict: A dictionary mapping author names to their corresponding email, aliases, and first commit date.
            before (str): Optional. A string representing the date before which to extract commits.
            after (str): Optional. A string representing the date after which to extract commits.

        """
        extracted_commits = GitCommit.extract_commits_from_git_log(
            self.path, before, after
        )
        self.commits = SquashedGitCommit.squash_consequent_commits(extracted_commits)
        self.__set_diffs()
        for commit in self.commits:
            for author in self.authors:
                if (author.email == commit.author.email) or (
                    commit.author.email in author.aliases
                ):
                    break
            else:
                for author in author_merge_dict:
                    if commit.author.email == author_merge_dict[author]["email"]:
                        commit.author.aliases = author_merge_dict[author]["devKeys"]
                        commit.author.first_commit_date = datetime.strptime(
                            author_merge_dict[author]["first_commit_date"],
                            "%Y-%m-%dT%H:%M:%SZ",
                        ).replace(tzinfo=pytz.utc)
                        commit.author.gh_username = author
                        break
                    elif commit.author.email in author_merge_dict[author]["devKeys"]:
                        commit.author.first_commit_date = datetime.strptime(
                            author_merge_dict[author]["first_commit_date"],
                            "%Y-%m-%dT%H:%M:%SZ",
                        ).replace(tzinfo=pytz.utc)
                        commit.author.gh_username = author
                        break
                else:
                    print(f"Author not found: {commit.author.email}")
                    commit.author.first_commit_date = commit.date
                self.authors.append(commit.author)

    def __set_diffs(self):
        progress_bar = tqdm(total=len(self.commits), desc="Setting diffs")
        for commit in self.commits:
            commit.set_diffs()
            progress_bar.update(1)
        progress_bar.close()

    def __str__(self):
        return f"{self.path} {self.commits} {self.authors} {self.files}"

    def analyze(self):
        """
        Analyzes the logs of the commits in the repository and calculates code survival rates for authors.

        Returns:
            tuple: A tuple containing the authors and files in the repository.

        """
        progress_bar = tqdm(total=len(self.commits), desc="Analyzing logs")
        for commit in self.commits:
            cur_author = None
            for author in self.authors:
                if (author.email == commit.author.email) or (
                    commit.author.email in author.aliases
                ):
                    cur_author = author
                    break
            else:
                raise Exception(f"Author not found: {commit.author.email}")

            for diff in commit.diffs:
                if diff.old_filename:
                    for old_file in self.files:
                        if old_file.name == diff.old_filename:
                            old_file.name = diff.filename
                            # print(f"Renamed file: {diff.old_filename} to {diff.filename} - {commit.commit_hash}")
                            break
                    else:
                        print(
                            f"Old file not found: {diff.old_filename}, {commit.commit_hash}"
                        )

                file = None
                for f in self.files:
                    if f.name == diff.filename:
                        file = f
                        # print(f"Found file: {diff.filename} - {commit.commit_hash}")
                        break
                else:
                    # print(
                    #    f"File not found: {diff.filename}, {commit.commit_hash}"
                    # )
                    file = GitFile(diff.filename, [])
                    self.files.append(file)

                for line in diff.lines:
                    try:
                        if line.operation == "+":
                            try:
                                file.lines.append(line)
                                if (
                                    commit.date
                                    < cur_author.first_commit_date
                                    + relativedelta(months=+MONTHS)
                                ) and commit.date >= cur_author.first_commit_date:
                                    cur_author.loc += 1
                            except Exception as e:
                                print(
                                    f"Error adding new line to author: {cur_author}: {e}"
                                )
                                exit()
                        elif line.operation == "-":
                            for old_line in file.lines:
                                if old_line.content == line.content:
                                    for author in self.authors:
                                        if author.email == old_line.author.email:
                                            try:
                                                if (
                                                    (
                                                        commit.date
                                                        < author.first_commit_date
                                                        + relativedelta(months=+MONTHS)
                                                    )
                                                    and commit.date
                                                    >= author.first_commit_date
                                                ):
                                                    author.dead_loc += 1
                                                break
                                            except Exception as e:
                                                print(
                                                    f"Error adding dead loc to author: {author}: {e}"
                                                )
                                                exit()
                                    file.lines.remove(old_line)
                                    break
                    except Exception as e:
                        print(f"An error occurred: {e}")

            progress_bar.update(1)

        progress_bar.close()

        for author in self.authors:
            if author.loc != 0:
                author.survival_rate = (author.loc - author.dead_loc) / author.loc

        return self.authors, self.files
