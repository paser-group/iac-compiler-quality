from google.cloud import bigquery
from google.oauth2 import service_account

key_path = "/data/minh/CompilierFuzzing/bigquery/plenary-chalice-375716-0c557fd8ab98.json"

credentials = service_account.Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)
client = bigquery.Client(credentials=credentials, project=credentials.project_id,)

# bucket_name = 'my-bucket'
# project = "githubsolidityquery"
# dataset_id  = "ansible_plays_github"
# table_id = "play_content_copy"
# destination_uri = "gs://{}/{}".format(bucket_name, "shakespeare.csv")
# dataset_ref = bigquery.DatasetReference(project, dataset_id)
# table_ref = dataset_ref.table(table_id)

# extract_job = client.extract_table(
#     table_ref,
#     destination_uri,
#     # Location must match that of the source table.
#     location="US",
# )  # API request
# extract_job.result()  # Waits for job to complete.

query = """
    EXPORT DATA OPTIONS(
    uri='gs://bucket/folder/*.csv',
    format='CSV',
    overwrite=true,
    header=true,
    field_delimiter=';') AS
    SELECT *
    FROM `githubsolidityquery.ansible_plays_github.play_content`
    LIMIT 20
"""

query_job = client.query(query)  # Make an API request.
results = query_job.result()  # Wait for query to complete.