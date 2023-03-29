# Google BigQuery Query and CSV Export with Python

This Python code demonstrates how to query a Google BigQuery table and export the results to a CSV file using the **`pandas`** library.

## Prerequisites
- A Google Cloud Platform account with a project set up
- A BigQuery table to query
- **`pandas`** library (**`pip install pandas`**)
- **`google-cloud-bigquery`** library (**`pip install google-cloud-bigquery`**)
- A service account key with access to the BigQuery table
## Usage
1. Set the path to the service account key file in the **`key_path variable`**.
2. Set the query to run in the **`query_string variable`**.
3. Set the output file path and name in the **`to_csv method`**.
4. Run the script.
5. The script will use the service account key to authenticate and authorize the query, retrieve the query results using **`pandas.read_gbq`**, and then export the results to a CSV file.
