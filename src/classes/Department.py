import os
import pandas as pd
import numpy as np
from datetime import datetime

class Department():
    def __init__(self, dept_num, yaml, police_csv_dir):

#### Initial config        
        self.dept_num = dept_num
        self.yaml = yaml
        self.police_csv_dir = police_csv_dir
        self.stdized_date_col_name = 'date'
        self.output_date_format = '%m/%d/%Y'
        self.city = yaml["police_csv_config"]["city"]
        self.state = yaml["police_csv_config"]["state"]
#### End initial conf
        print("creating dept # {}".format(self.dept_num))
        self.input_police_df = self.get_input_police_df()
        
    def get_input_police_df(self):

        dept_num = self.dept_num
        police_csv_dir = self.police_csv_dir
        yaml = self.yaml
        
        dept_folder = os.path.join(police_csv_dir, "Dept_{}".format(dept_num))
        dept_folder_exists = os.path.isdir(dept_folder)

        if dept_folder_exists:

            csvs = [f for f in os.listdir(dept_folder) if f.endswith('.csv')]
            police_csv_filename = csvs[0]
            if len(csvs) != 1:
                print("WARNING: Dept {} has more than one CSV. Using {} to read in police encounter data".format(dept_num, police_csv_filename))

            police_csv_full_path = os.path.join(dept_folder, police_csv_filename)
            police_df = pd.read_csv(police_csv_full_path, skiprows=yaml['police_csv_config']['header_row_idx'])
            
        return police_df
    
    def get_standardized_police_df(self):
        
        input_police_df = self.input_police_df
        standardized_col_police_df = input_police_df
        yaml = self.yaml
        
        police_csv_columns_dict = yaml['police_csv_columns']
        police_csv_config = yaml['police_csv_config']
        if police_csv_config.get('skip_first_row') == True:
            standardized_col_police_df = standardized_col_police_df[1:]
        
        cols_to_keep = [col for col in list(police_csv_columns_dict.keys()) if police_csv_columns_dict[col] is not None]
        
        for k, v in police_csv_columns_dict.items():
            
            if v is None:
                continue
            if isinstance(v, list):
                standardized_col_police_df[k] = standardized_col_police_df[v].apply(lambda x: ','.join([str(elem) for elem in x if not pd.isnull(elem)]), axis=1)
                standardized_col_police_df = standardized_col_police_df.drop(columns=v)
            else:
                standardized_col_police_df = standardized_col_police_df.rename(index=str, columns = {v : k})

        standardized_col_police_df["dept"] = self.dept_num
        standardized_col_police_df["city"] = self.city
        standardized_col_police_df["state"] = self.state
        standardized_col_police_df = standardized_col_police_df[["dept", "city", "state"] + cols_to_keep]
        
        return standardized_col_police_df

    def standardize_date_col(self, df):
        
        date_col_name = self.stdized_date_col_name
        output_date_format = self.output_date_format
        yaml = self.yaml
        
        date_format = yaml['police_csv_config']['date_format']
        df[date_col_name] = pd.to_datetime(df[date_col_name], format=date_format)

        return df