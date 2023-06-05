# external imports
import requests
import json
from datasets import Dataset
from tqdm import tqdm
from typing import List, Dict

class GithubScraper:

    def __init__(self, cfg: Dict):
        
        # initialize variables for querying github
        self.token = cfg['github']['token']
        self.repo_owner = cfg['github']['repo_owner']
        self.repo_name = cfg['github']['repo_name']

    def get_issue_data(self, issue_id: int) -> Dict:
        """
        used to get the desired github issue data

        Input: 
            issue_id[int]: the target issue id

        Return:
            data[Dict]: a dictionary with the gihub body and comments for <issue_id>
        """

        # get issue body
        issue_url = \
            f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_id}"
        issue = get_response(
            token=self.token,
            url=issue_url
        )
        issue_body = issue['body']

        # get issue comments
        comment_url = issue['comments_url']
        comments = get_response(
            token=self.token,
            url=comment_url
        )
        comment_bodies = [comment['body'] for comment in comments]

        # consolodate data into dictionary
        data = {
            'body' : issue_body,
            'comments' : comment_bodies
        }

        return data


    def collect_commits(
        self,
        n_samples: int=100,
        ver: str='stable-2.14',
        progbar: bool=False,
        retry_limit: int=3
    ) -> Dataset:
        """
        collects <n_samples> latest commits from branch <ver>.

        Input:
            n_samples[int]: number of samples to collect
            ver[str]: the target github branch
            progbar[bool]: defines wheteher to use a progress bar for collecting diffs
            retry_limit[int]: retry limit for collecting the diff text

        Return:
            commit_history[Dataset]: the target commit history
        """

        # collect commit history for given version
        trgt_url = \
            f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/commits"
        progress = 0
        page=1
        commits = []
        while True:
            if progress >= n_samples:
                break

            # attempt to get more commits
            batch = get_response(
                token=self.token,
                url=trgt_url,
                params={
                    'sha': ver,
                    'page': page
                }
            )

            if batch is None: break

            # update commits list and increment counters
            commits += batch
            page += 1
            progress = len(commits)

        # truncate commits to number of requested samples
        commits = commits[:n_samples]

        # consolidate into desired fields
        data = [
            {
                'sha': commit['sha'],
                'commit_msg': commit['commit']['message'],
                'api_url': commit['url'],
                'html_url': commit['html_url'],
            }
            for commit in commits
        ]

        # convert data to dataset
        ds = Dataset.from_list(data)

        # decide whether to use a progress bar or not
        diffs = []
        iterator = \
            tqdm(ds, total=len(ds), desc='collecting diff text') if progbar \
            else ds
            
        # get diff data using standard request
        for sample in iterator:
            # loop to retry requests
            for _ in range(retry_limit):
                diff = requests.get(
                        f"https://github.com/{self.repo_owner}/{self.repo_name}"
                        + f"/commit/{sample['sha']}.diff"
                )
                if diff is not None: break
            
            diffs.append(
                diff.text if diff is not None
                else ''
            )

        ds = ds.add_column('diff_text', diffs)
        return ds

    def list_branches(self, per_page: int=100) -> List:
        """
        requests a list of branches from the github API.
        NOTE: this isn't really used but may come in handy later

        Input:
            per_page: the page limit of the request. range is 100 >= per_page >= 1
        
        Return
            response[Dict]: the http/https response 
        """
        trgt_url = \
            f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/branches"
        response = get_response(
            token=self.token,
            url=trgt_url,
            params={
                'per_page': per_page,
            },
        )

        return response

""" helper functions """

def get_response(
    token: str,
    url: str,
    headers: Dict={},
    params: Dict=None
) -> Dict | List: 
    """
    takes in a url and token and returns the http/https response.
    NOTE: this is only really meant for the github api due to a static header that's used
    
    Input:
        token[str]: the github api token
        url[str]: the target github url
        headers[Dict]: any custom headers that need to be added
        params[Dict]: any custom parameters that need to be added

    Return
        response[Dict]: the json version of the http/https response
    """

    headers.update({
        'Authorization': f'Token {token}'
    })

    response = requests.get(
        url,
        headers=headers,
        params=params,
    )
    if response.status_code == 200:
        data = response.json()
    else:
        data = None 

    return data
