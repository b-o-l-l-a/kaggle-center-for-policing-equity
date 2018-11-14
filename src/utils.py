import pandas as pd
import os
import yaml

def get_depts(yaml_dir):
    
    dept_list = [f.replace(".yml", "") for f in os.listdir(yaml_dir) if f.endswith('.yml') and f != 'template.yml']
    
    return dept_list

def get_dept_yaml(yaml_dir, dept_num):
    
    dept_yaml = os.path.join(yaml_dir, "{}.yml".format(dept_num))
    yaml_in = yaml.load(open(dept_yaml))

    return yaml_in