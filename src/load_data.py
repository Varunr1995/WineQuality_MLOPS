# Read the data from data source
# Save it in the data/raw for further process

import os
from get_data import read_params, get_data # These are the variables in the other python file
import argparse
import yaml

def load_and_save(config_path): # The reason to provide config_path is as the code expects a configuration file to process the data.
    config = read_params(config_path)
    df = get_data(config_path)
    # new_cols = [col for col in df.columns] # This will help in printing the column names of the dataframe.
    # print(new_cols)
    new_cols = [col.replace(" ","_") for col in df.columns] # We are trying to replace the space value with other character
    raw_data_path = config["load_data"]["raw_dataset_csv"]
    df.to_csv(raw_data_path, sep=",", index=False, header=new_cols) # The changes gets updated and creates a new .csv file in the data/raw folder.

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()
    load_and_save(config_path=parsed_args.config)
