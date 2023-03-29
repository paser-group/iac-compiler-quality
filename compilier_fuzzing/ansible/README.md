# Ansible GitHub Issues Downloader
This Python script downloads closed issues from a GitHub repository with a given label, and saves them as a feather or csv file.

## Prerequisites
- **`requests`** module (install with pip install requests)
- **`tqdm`** module (install with pip install tqdm)
- A GitHub Personal Access Token with repo permissions

## Usage
1. Open the script in a text editor and fill in the following variables at the top of the script:

- **`repo_owner`**: The owner of the GitHub repository (e.g., ansible)
- **`repo_name`**: The name of the GitHub repository (e.g., ansible)
- **`token`**: Your GitHub Personal Access Token with repo permissions
- **`label`**: The label to filter issues by (e.g., bug)

2. Run the script with the following command: python **`github_issues_downloader.py`**
3. The script will start downloading closed issues with the given label from the GitHub repository. Progress will be displayed with a progress bar.
4. When the script is finished, it will save the downloaded issues as a feather file in the data/github_issues/ directory with the name github_issues.feather.
5. You can load the downloaded issues from the feather file with pd.read_feather.
