from eduki_data_engineering.utils.data_processor import DataProcessor
from eduki_data_engineering.utils.config_parsers import get_ini_config_object
from eduki_data_engineering.utils.postgresql_bulk_writer import PostgreSQLBulkWriter
import logging 


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class PostgreSQLIngestionOperator(DataProcessor):

    def __init__(
            self, 
            ) -> None:
        super().__init__(input_path_key='revenue_csv_path')
        self.PSQL = PostgreSQLBulkWriter(table_name='query_results_pgtable')

        log.info(' Initializing PostgreSQLIngestionOperator... ')

    def write_data(self):
        super().write_data()
        self.PSQL.insert_data(self.transformed_data)
        log.info(' Process ended successfully')

    def main_process(self):
        #Extract & Load
        self.load_data()
        #Transform
        self.transform_data()
        #Ingest
        self.write_data()
        
    

if __name__=="__main__":
    p=PostgreSQLIngestionOperator()
    p.main_process()




