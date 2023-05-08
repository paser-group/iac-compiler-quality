from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

key_path = "/data/minh/CompilierFuzzing/bigquery/plenary-chalice-375716-0c557fd8ab98.json"

credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

# query = """
#     SELECT name, SUM(number) as total_people
#     FROM `bigquery-public-data.usa_names.usa_1910_2013`
#     WHERE state = 'TX'
#     GROUP BY name, state
#     ORDER BY total_people DESC
#     LIMIT 20
# """
# query_job = client.query(query)  # Make an API request.
# print("The query data:")
# for row in query_job:
#     # Row values can be accessed by field name or index.
#     print("name={}, count={}".format(row[0], row["total_people"]))

query = """
    SELECT *
    FROM `githubsolidityquery.ansible_plays_github.play_content`
    LIMIT 20
"""

query_job = client.query(query)  # Make an API request.
results = query_job.result()  # Wait for query to complete.

print("Total rows {}".format(results.total_rows))
