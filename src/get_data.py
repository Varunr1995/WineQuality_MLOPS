## read the params
## process
## return dataframe

import os
import yaml
import pandas as pd
import numpy as np
import argparse

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def get_data(config_path):
    config = read_params(config_path)
    data_path = config["data_source"]["s3_source"] # Need to provide the path of the file which holds the data file from params.yaml
    df = pd.read_csv(data_path, sep=',', encoding='utf-8')
    # print(df.head()) # Once we printed the data frame we need to comment the pandas dataframe and need to return the data frame.
    return df
    

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()
    data = get_data(config_path=parsed_args.config)