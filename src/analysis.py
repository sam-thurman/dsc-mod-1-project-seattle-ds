import os
import sys
module_path = os.path.abspath(os.path.join(os.pardir, os.pardir))
if module_path not in sys.path:
    sys.path.append(module_path)
    
import psycopg2
import pandas as pd

def example(csv_file):

    dir = os.path.dirname(__file__)
    relative_filename = os.path.join(dir, 'data', csv_file)

    print (relative_filename)
    df = pd.read_csv(relative_filename)

    return df

def import_final_metrics(csv_file):
    relative_filename = os.path.abspath(os.path.join(os.pardir, os.pardir, 'data_files', csv_file))
    
    df = pd.read_csv(relative_filename)
    df = df.drop(['Unnamed: 0'], axis=1)
    return df