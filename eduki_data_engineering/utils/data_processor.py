from abc import ABC, abstractmethod
from eduki_data_engineering.utils.config_parsers import (
    get_ini_config_object,
    load_schema_from_yaml,
)
import pandas as pd
from typing import List, Dict, Tuple
from datetime import datetime
from logging import Logger, getLogger
from logging.config import fileConfig
from os.path import abspath, dirname, join
from eduki_data_engineering.utils.eduki_root_logger import configure_root_logger
import logging

configure_root_logger(log_level=logging.INFO)
log = logging.getLogger(__name__)

class DataProcessor(ABC):

    def __init__(
            self,
            input_path_key:str,
            output_path_key:str = None,
            ) -> None:
        self.io_paths = self._get_paths(input_path_key,output_path_key)
        


    def _get_paths(self,input_path_key : str , output_path_key : str = None ):
        return (
            get_ini_config_object('paths')['input_data'][input_path_key],
            get_ini_config_object('paths')['output_data'][output_path_key] if output_path_key else None
        )
    
    
    def load_data(self):
        """
        Reads tabular CSV data and loads it into Pandas df object.
        """
        # - With low_memory=False we increase memory usage 
        # but overall we get better performance and processing speeds
        log.info(' Loading input data from CSV (Local machine) ...')
        self.input_data = pd.read_csv(self.io_paths[0], low_memory = False ) 


    def detect_quartiles(self):
        quartiles = self.input_data["revenue"].quantile([0.25, 0.5, 0.75])
        return [quartiles[q] for q in [0.25, 0.5, 0.75]]
    
    @staticmethod
    def classify_revenue_from_sorted_classes(revenue_value : float , revenue_classes: List[Tuple]):
        """
        Binary Search on the Sorted List of Q thresholds.
        Static method to be used ad-hoc for pandas operations
        """
        for tier, q_threshold in revenue_classes:
            if revenue_value <= q_threshold:
                return tier
    

    def revenue_classification(self, data):

        (Q1,Q2,Q3) = self.detect_quartiles()
        
        # Group revenue-tiers and thresholds to list of tuples
        # in sorted way for efficiency

        revenue_classes = [
                ("Low", Q1), # <= Q1,
                ("Mid Low", Q2), # <= Q2
                ("Mid High", Q3), # <= Q3
                ("High", float("inf"))   # >Q3
            ]
        log.info(' Classifying revenue...')
        # Construct revenue-classes column (categorical)
        data["revenue_class"] = data["revenue"].apply(lambda x : self.classify_revenue_from_sorted_classes(x, revenue_classes)).astype("category")
        return data

    def calculate_avg_revenue(self):
        log.info(' Calculate average revenue per tier...')
        # Grouped table that assignes mean avg to revenue classes
        average_revenue_per_class = self.transformed_data.groupby("revenue_class", observed=False)["revenue"].mean().reset_index()
        # Merge this data by joining the two tabular structures
        self.transformed_data= self.transformed_data.merge(average_revenue_per_class, on="revenue_class", how="left", suffixes=("", "_class_avg"))

    def add_ingestion_date(self):
        """
        As a fast monitoring feature (to avoid new tables)
        here we insert the current ingestion date & time.
        [Example format : 2024-04-20_22:30:45 ]
        """
        self.transformed_data['ingestion_datetime'] = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    def enforce_schema(self):
        schema = load_schema_from_yaml()
        for col, dtype in schema.items():
            if not 'datetime' in dtype:
                self.transformed_data[col] = self.transformed_data[col].astype(dtype)
            else :
                self.transformed_data[col] = pd.to_datetime(self.transformed_data[col], format='%Y-%m-%d_%H:%M:%S')

    def transform_data(self):
        """
        Compile all data operations 
        and generate final self.transformed_data
        """
        log.info(' Transforming dataset...')
        self.transformed_data = self.revenue_classification(data=self.input_data)
        self.calculate_avg_revenue()
        self.add_ingestion_date()
        self.enforce_schema()


    @abstractmethod
    def write_data(self):
        """
        Flexible and essential method to be always implemented in our code 
        (thuss the abstract decorator).
        It writes data to an output database, data warehouse etc.
        """
        log.info(' Back-ing up data operations in action...')


