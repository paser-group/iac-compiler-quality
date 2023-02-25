import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

key_path = "/data/minh/CompilierFuzzing/bigquery/plenary-chalice-375716-0c557fd8ab98.json"

credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

query_string = """
    SELECT * 
    FROM `githubsolidityquery.ansible_plays_github.play_content` 
    LIMIT 1000
"""

df = pd.read_gbq(query_string, credentials=credentials)
df.to_csv('/data/minh/CompilierFuzzing/data/github_data.csv')
print('Done')