import requests
from tqdm import tqdm

def download_issues(repo_owner, repo_name, label, token=None):
    issues = []
    page = 1
    headers = {}
    if token:
        headers = {
            "Authorization": f"Token {token}"
        }
    with tqdm(total=None, desc="Fetching Issues") as pbar:
        while True:
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues?state=closed&labels={label}&exclude=pulls&page={page}&per_page=100"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                issues.extend([{"title": issue["title"], "body": issue["body"]} for issue in data if "pull_request" not in issue])
                pbar.update(len(data))
                page += 1
            else:
                break
        return issues
    
repo_owner = "ansible"
repo_name = "ansible"
token = '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'
issues = download_issues(repo_owner, repo_name,  label='bug', token=token)
print("Number of issues:", len(issues))


import pandas as pd
import os  

df = pd.DataFrame(issues)
# df.to_feather('../data/github_issues/github_issues.feather')
# ndf = pd.read_feather('../data/github_issues/github_issues.feather')

# os.makedirs('../data/github', exist_ok=True)  
df.to_csv('../data/github/issues.csv') 