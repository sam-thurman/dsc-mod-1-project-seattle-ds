import os
import sys
module_path = os.path.abspath(os.path.join(os.pardir, os.pardir))
if module_path not in sys.path:
    sys.path.append(module_path)
    
import psycopg2
import pandas as pd



def return_df(csv_file):

    dir = os.path.dirname(__file__)
    relative_filename = os.path.join(dir, 'data', csv_file)

    print (relative_filename)
    df = pd.read_csv(relative_filename)

    return df


def return_df2(csv_file):
    relative_filename = os.path.abspath(os.path.join(os.pardir, 'data_files', csv_file))

    return relative_filename