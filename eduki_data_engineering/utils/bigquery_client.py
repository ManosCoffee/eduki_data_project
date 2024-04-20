from google.cloud import bigquery
from google.oauth2 import service_account
from eduki_data_engineering.utils.config_parsers import (
    set_gcp_credentials,
    set_eduki_bq_table,
)
import pyarrow.parquet as pq
import pandas_gbq as bq 
from logging import Logger, getLogger
from logging.config import fileConfig


fileConfig("configs/logging.ini")
log: Logger = getLogger()

@set_gcp_credentials()
@set_eduki_bq_table()
class BigQueryClient(bigquery.Client):
    """
    BQ Client class extention that automatically connects 
    to project . It enables the user to write to bq table 
    using load_dataframe_to_table.
    """
    def __init__(self, **kwargs):
        gcp_service_credentials = service_account.Credentials.from_service_account_info(BigQueryClient.GCP_CREDENTIALS)
        super().__init__(
            project=BigQueryClient.GCP_CREDENTIALS['project_id'], 
            credentials=gcp_service_credentials
            )
        
    
    def ingest_data_to_bq(self, dataframe, schema):
        """
        Main ingestion method, utilizing GCP connection from BQ client,
        that writes data by transforming them internally to parquets.
        """
        log.info(f' Ingesting {dataframe.shape[0]} rows to BigQuery table : {BigQueryClient.BQ_TABLE_ID.split(".")[-1]}')
        # Convert DataFrame to Parquet file (temp)
        # pq.write_table(pq.Table.from_pandas(dataframe), './tmp.parquet')
        bq.to_gbq(
            dataframe = dataframe,
            destination_table=BigQueryClient.BQ_TABLE_ID, 
            project_id= BigQueryClient.GCP_CREDENTIALS['project_id'], #'eduki-420720', 
            if_exists='append',
            credentials=self._credentials,
            api_method="load_csv",
            table_schema = schema
            )
        
    def get_row_count(self):
        """
        Checks how many rows we ingested.
        """
        query = f"""
        SELECT COUNT(*) as row_count FROM `{BigQueryClient.GCP_CREDENTIALS['project_id']}.{BigQueryClient.BQ_TABLE_ID}`
        """
        df = bq.read_gbq(query, project_id=BigQueryClient.GCP_CREDENTIALS['project_id'])
        return df['row_count'][0]

   