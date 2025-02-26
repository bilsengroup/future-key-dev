# git-mine

This directory contains a Git log analysis tool that helps you analyze the code survival rates of each developer by using the commit history of a Git repository. 

It requires Python 3.9 or higher and Git to be installed on your system. Additionally, make sure to install the required packages listed in the `requirements.txt` file.

To use the tool, follow these steps:

1. Clone the Git repository you want to analyze.
2. Open a terminal or command prompt and navigate to the directory where the `git-mine.py` script is located.
3. Run the following command:

```
python git-mine.py --path /path/to/git/repository --authors /path/to/authors/file
```

Replace `/path/to/git/repository` with the actual path to your Git repository and `/path/to/authors/file` with the path to the authors file.

An example JSON file named `example_author.json` can be found in this directory, showing the structure of key-value pairs in an authors file. An authors file for a repository can be obtained by running the scripts under the [method1](../../method1) folder in this repository. Please refer to the respective [README.md](../../method1/README.md) file for further instructions.

The tool will analyze the Git log and output the results to a file named `devs.csv`.

`git-mine.py` is the main script of the Git log analysis tool. It takes command-line arguments to specify the path to the Git repository and the authors file. It uses the `classes.py` module to perform the analysis and generate the output.

`classes.py` contains the necessary classes and functions for analyzing the Git log. It provides methods to extract information about commits, authors, and other relevant data.
