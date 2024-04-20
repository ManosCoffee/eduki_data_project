import psycopg2
from psycopg2.extras import execute_batch
import pandas as pd
from eduki_data_engineering.utils.config_parsers import set_postgres_credentials
import numpy as np
from typing import List
from logging import Logger, getLogger
from logging.config import fileConfig


fileConfig("configs/logging.ini")
log: Logger = getLogger()


@set_postgres_credentials()
class PostgreSQLBulkWriter:
    def __init__(self, table_name):
        """
        Initialize the PostgresBulkInsert object.
        """
        self.table_name = table_name

    def create_column_if_not_exists(self, column: str,cur, conn):
    # Check if the column exists
        cur.execute(f"""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.columns 
                WHERE table_name = '{self.table_name}' 
                AND column_name = '{column}'
            )
        """)
        column_exists = cur.fetchone()[0]

        # If column doesn't exist, create it
        if not column_exists:
            cur.execute(f"""
                ALTER TABLE {self.table_name} 
                ADD COLUMN IF NOT EXISTS {column} VARCHAR(255)
            """)
            conn.commit()


    def insert_data(self, df):
        """
        Insert data from a DataFrame to a PostgreSQL table using bulk insertion.
        """
        conn = psycopg2.connect(**PostgreSQLBulkWriter.POSTGRESQL_CREDENTIALS)
        cur = conn.cursor()

        try:
            # Define the SQL query with placeholders for parameters
            columns = ', '.join(df.columns)
            placeholders = ', '.join(['%s'] * len(df.columns))

            log.info(f' Checking for new columns and updating {self.table_name}')
            # Check for new columns (create)
            for col in ['revenue_class','revenue_class_avg','ingestion_datetime']:
                self.create_column_if_not_exists(col,cur=cur, conn=conn)

            sql = f"""
                        INSERT INTO {self.table_name} 
                        ({columns}) 
                        VALUES ({placeholders})
                    """
            data = [tuple(row) for row in df.to_numpy()]
            # Execute the SQL query 
            log.info(' Executing insertion...')
            execute_batch(cur, sql, data)
            # Send Transaction
            conn.commit()

        finally:
            # Close connection
            cur.close()
            conn.close()

