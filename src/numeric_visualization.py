# importing packages

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns


def import_and_assign():
  # assigning 'groomed' csv data to variables as dataframes
  
  ay_df = pd.read_csv('ay_df.csv')
  oy_df = pd.read_csv('oy_df.csv')
  full_dfs = [ay_df, oy_df]
  #racial df
  racial_df = pd.read_csv('racial_data.csv')

  # age dfs
  ay_df_16_18 = pd.read_csv('ay_df_16_18.csv')
  ay_df_19_21 = pd.read_csv('ay_df_19_21.csv')
  ay_df_22_24 = pd.read_csv('ay_df_22_24.csv')
  oy_df_16_18 = pd.read_csv('oy_df_16_18.csv')
  oy_df_19_21 = pd.read_csv('oy_df_19_21.csv')
  oy_df_22_24 = pd.read_csv('oy_df_22_24.csv')
  age_df_dict = {'total_youth':[ay_df_16_18, ay_df_19_21, ay_df_22_24],'opportunity_youth':[oy_df_16_18, oy_df_19_21, oy_df_22_24]}
  return full_dfs, racial_df, age_df_dict

def plot_16_v_20():
  plt.bar(['2016', '2020'], [18817, 11115])
  plt.title('Number of OY in SKC 2016 vs. 2020')

def plot_oy_by_age(age_df_dict):
  age_group_strings = ['16-18', '19-21', '22-24']
  ay_age_group_val_list = [age_df_dict['total_youth'][0]['pwgtp'].sum(),
                        age_df_dict['total_youth'][1]['pwgtp'].sum(),
                        age_df_dict['total_youth'][2]['pwgtp'].sum()]

  oy_age_group_val_list = [age_df_dict['opportunity_youth'][0]['pwgtp'].sum(),
                        age_df_dict['opportunity_youth'][1]['pwgtp'].sum(),
                        age_df_dict['opportunity_youth'][2]['pwgtp'].sum()]
  oy_percentage_of_age_pop = [int(o) / int(y) for o,y in zip(oy_age_group_val_list, ay_age_group_val_list)]
  oy_percentage_of_age_pop = [x*100 for x in oy_percentage_of_age_pop]
  plt.ylim(0,50)
  plt.bar(age_group_strings, oy_percentage_of_age_pop)
  plt.title('Percent Representation of OY in Age Group ')
  plt.xlabel('Age Group')
  plt.ylabel('Percent of Age Group')