from configparser import ConfigParser
import re
import logging
import os
import json
from typing import Dict
from logging import Logger, getLogger
from logging.config import fileConfig
import yaml

log: Logger = getLogger()



def get_ini_config_object(config_name : str) -> ConfigParser:
    """
    Parses config.ini file and
    returns a configuration object.
    """
    config = ConfigParser()
    config.read(f"configs/{config_name}.ini")
    return config


def replace_env_vars(value) -> str:
    """
    Generic helper method to detect and replace environemnt 
    variables with corresponding text.
    """
    def replace(match):
        env_var = match.group(1)
        return os.getenv(env_var, "")

    return re.sub(r'\${(\w+)}', replace, value)


def parse_config_string( config :ConfigParser , config_section: str, config_key: str)-> str:
    """
    Returns assigned value from a config ini object. Additionally it extracts
    any path-string from an environment variable, where it exists.
    """
    value = config[config_section][config_key]

    try : 
        return replace_env_vars(value)

    except Exception as e:
        log.error(e)
        return None 
    
    
def parse_config_to_dict(config) ->Dict:
    """
    Parser that reads config obeject,
    replaces ENV variables with their values
    and returns a dictionary obeject.
    """
    config_dict = {}
    for section in config.sections():
        config_dict[section]={}
        for key, value in config.items(section):
            config_dict[section][key] = replace_env_vars(value)

    return config_dict


def set_gcp_credentials():
    """
    Decorator that automatically sets GCP credentials 
    as class variables
    """
    def _set_gcp_credentials_decorator(cls):
        try:
            gcp_conf = get_ini_config_object('google_service_credentials')
            gcp_dictionary = parse_config_to_dict(gcp_conf)
            cls.GCP_CREDENTIALS = {**gcp_dictionary['google_cloud'],**gcp_dictionary['service_account']}

        except Exception:
            raise
        return cls

    return _set_gcp_credentials_decorator



def set_postgres_credentials():
    """
    Decorator that automatically sets GCP credentials 
    as class variables
    """
    def _set_postgres_credentials_decorator(cls):
        try:
            psql_conf = get_ini_config_object('postgresql_parameters')
            psql_dictionary = parse_config_to_dict(psql_conf)
            cls.POSTGRESQL_CREDENTIALS = {
                 **psql_dictionary['identity'],
                 **psql_dictionary['connection'],
                 **psql_dictionary['databases']
                 }
            
        except Exception:
            raise
        return cls

    return _set_postgres_credentials_decorator


def load_schema_from_yaml():
    with open('configs/sql_schema.yml', 'r') as yaml_file:
        schema = yaml.safe_load(yaml_file)
    return schema

def load_bq_schema_from_yaml():
    with open('configs/bq_schema.yml', 'r') as yaml_file:
        schema = yaml.safe_load(yaml_file)
    return schema


def generate_schema_for_bigquery():

    dtypes_mapping= load_bq_schema_from_yaml()
    return [{'name': field, 'type': dtypes_mapping[field]} for field in dtypes_mapping]

def set_bq_schema():
    """
    Decorator that automatically sets GCP credentials 
    as class variables
    """
    def _set_bq_schema_decorator(cls):
        try:
            cls.BQ_SCHEMA = generate_schema_for_bigquery()

        except Exception:
            raise
        return cls

    return _set_bq_schema_decorator

def set_eduki_bq_table():
    """
    Decorator that automatically sets BQ table info 
    as class variables
    """
    def _set_eduki_bq_table_decorator(cls):
        try:
            bq_conf = get_ini_config_object('big_query')
            bq_table_name = bq_conf['tables']['eduki_revenue_table']
            bq_dataset_id = bq_conf['datasets']['eduki_dataset_id']
            cls.BQ_TABLE_ID =f"{bq_dataset_id}.{bq_table_name}"
        except Exception:
            raise
        return cls

    return _set_eduki_bq_table_decorator










