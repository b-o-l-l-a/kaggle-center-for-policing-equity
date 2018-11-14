import pandas as pd
import os
import argparse
from classes.Department import Department 
from utils import get_depts, get_dept_yaml

def standardize_police_data(yaml_dir, police_dir, output_dir):
    
    dept_list = get_depts(yaml_dir)
    output_df = pd.DataFrame()
    trimmed_output_df = pd.DataFrame()
    
    for dept_num in dept_list:
        
        dept_yaml = get_dept_yaml(yaml_dir, dept_num)        
        dept = Department(dept_num, dept_yaml, police_dir)
        dept_stdized_df = dept.get_standardized_police_df()
        dept_stdized_df = dept.standardize_date_col(dept_stdized_df)
        trimmed_output_df = trimmed_output_df.append(dept_stdized_df[0:100], ignore_index=True)
        output_df = output_df.append(dept_stdized_df, ignore_index=True)
    
    output_path = os.path.join(output_dir, "step1_combined_police_data.csv")
    
    first_cols = ["dept", "city", "state"]
    output_df_cols = [col for col in output_df.columns if col not in first_cols]
    output_df = output_df[first_cols + output_df_cols]
    trimmed_output_df = trimmed_output_df[first_cols + output_df_cols]
    
    trimmed_output_df.to_csv(os.path.join(output_dir, "step1_combined_police_data_trimmed.csv"), index=False)
    output_df.to_csv(output_path, index=False)
    print("dropped CSV to {}".format(output_path))
    
    return

if __name__ == "__main__":
    
    default_yaml_dir = os.getcwd().replace("/src", "/data/department_yamls")
    default_police_dir = os.getcwd().replace("/src", "/data/raw_updated")
    default_output_dir = os.getcwd().replace("/src", "/data/interim")
    parser = argparse.ArgumentParser(description='Standardize police data into one comprehensive format')
    parser.add_argument("-y", "--yaml_dir", default=default_yaml_dir, 
        help="directory of yaml files for all depts to standardize. Defaults to {}".format(default_yaml_dir))    
    parser.add_argument("-p", "--police_dir", default=default_police_dir, 
        help="directory of police encounter CSVs. Defaults to {}".format(default_police_dir))
    parser.add_argument("-o", "--output_dir", default=default_output_dir,
        help="directory to drop combined CSV. Defaults to {}".format(default_output_dir))
    
    args = parser.parse_args()   
    
    standardize_police_data(args.yaml_dir, args.police_dir, args.output_dir)
