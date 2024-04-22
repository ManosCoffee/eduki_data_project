import pandas as pd
from google.cloud import bigquery
import time
from eduki_data_engineering.utils.bigquery_client import BigQueryClient
from eduki_data_engineering.utils.data_processor import DataProcessor
from eduki_data_engineering.utils.config_parsers import (
    set_bq_schema,
    set_eduki_bq_table,
)
import logging 

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


@set_bq_schema()
class BigQueryIngestionOperator(DataProcessor) :

    def __init__(
            self, ):
        super().__init__(input_path_key='revenue_csv_path' )
        self.Client = BigQueryClient()


    def write_data(self):
        super().write_data()
        self.Client.ingest_data_to_bq(
            dataframe=self.transformed_data,
            schema = BigQueryIngestionOperator.BQ_SCHEMA
        )

        log.info(' Process ended successfully: \n')
        log.info(f'Ingested : {self.Client.get_row_count()} rows!')


    def main_process(self):
        #Extract & Load
        self.load_data()
        #Transform
        self.transform_data()
        #Ingest
        self.write_data()

if __name__=="__main__":
    p=BigQueryIngestionOperator()
    p.main_process()
        