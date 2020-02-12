# importing packages

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
DBNAME = 'opportunity_youth'
conn = psycopg2.connect(dbname=DBNAME)


#       assign 'groomed' csv data to variables as dataframes
def import_and_assign(): 
  # df of ALL youth (age 16-24) in South King County
  ay_df = pd.read_csv('ay_df.csv')
   # df of OPPORTUNITY youth (age 16-24) in South King County
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


#       generate bar plot: number of opportunity youth in SKC in 2016 vs. 2020
def plot_16_v_20(full_dfs):
  num_oy_2016 = 18817
  plt.bar(['2016', '2020'], [num_oy_2016, full_dfs[1]['pwgtp'].sum()])
  plt.title('Number of OY in SKC 2016 vs. 2020')


#       group ay_df and oy_df by age groups, return list of OY percent 
#       representation in each age group and list of age group strings
def get_age_plot_reqs(age_df_dict):
  age_group_strings = ['16-18', '19-21', '22-24']
  ay_age_group_val_list = [age_df_dict['total_youth'][0]['pwgtp'].sum(),
                          age_df_dict['total_youth'][1]['pwgtp'].sum(),
                          age_df_dict['total_youth'][2]['pwgtp'].sum()]

  oy_age_group_val_list = [age_df_dict['opportunity_youth'][0]['pwgtp'].sum(),
                          age_df_dict['opportunity_youth'][1]['pwgtp'].sum(),
                          age_df_dict['opportunity_youth'][2]['pwgtp'].sum()]
  oy_percentage_of_age_pop = [int(o) / int(y) for o,y in zip(oy_age_group_val_list, ay_age_group_val_list)]
  oy_percentage_of_age_pop = [x*100 for x in oy_percentage_of_age_pop]
  return ay_age_group_val_list, oy_age_group_val_list, oy_percentage_of_age_pop, age_group_strings


#       generate bar plot:percent of age group representated in OY population
def plot_percent_oy_by_age(oy_percentage_of_age_pop, age_group_strings):
  plt.ylim(0,50)
  plt.bar(age_group_strings, oy_percentage_of_age_pop)
  plt.title('Opportunity Youth {%} representation in each age group')
  plt.xlabel('Age Group')
  plt.ylabel('Percent of Age Group')


#     generate bar plots: 
#       age stats for AY & OY aswell as percent of age group 
#       representated in OY population
def plot_in_depth_age(oy_age_group_val_list, ay_age_group_val_list, age_group_strings, oy_percentage_of_age_pop):
  sns.set_style("darkgrid")
  fig, axes = plt.subplots(1, 3, figsize=(20,6))
  axes[0].set_ylim(0,35000)
  axes[1].set_ylim(0,35000)
  axes[2].set_ylim(0,50)
  sns.barplot(y = oy_age_group_val_list, 
              x = age_group_strings, 
              ax = axes[0]).set_title('Number of Opportunity Youth by Age in South King County', fontsize=15)
  sns.barplot(y = ay_age_group_val_list, 
              x = age_group_strings, 
              ax = axes[1]).set_title('Number of Non-Opportunity Youth by Age in South King County', fontsize=15)
  sns.barplot(y = [x*100 for x in oy_percentage_of_age_pop], 
              x = age_group_strings,
              ax = axes[2]).set_title('Opportunity Youth Percent of Pop. by Age', fontsize=15)
  axes[2].set_ylabel('percent of total age group')
  plt.subplots_adjust(wspace = 0.6) 


#       rename columns of racial_df to be camel case so they can be called 
#       accessed w pandas
def rename_race_df_columns(racial_df):
  racial_df.columns = ['unnamed', 'Race',  'rate_of_oy', 'total_youth_pop',  'proportion_of_oy', 'oy_total']
  return racial_df


#     generate bar plots:
#       breakdown of AY % representation by race and breakdown of OY % representation by race
def plot_racial_representation(racial_df):
  rename_race_df_columns(racial_df)
  fig, ax = plt.subplots(1,2,figsize=(15,6))
  race_palette = {'White':'#87FFF6', 'Hispanic':'#A6E87B', 'African American':'#FFE294', 'Asian':'#E88D7B', 'Two or More Races':'#DD9EFF', 'Other Race':'#A187FF', 'Native American or Alaska Native':'#7BE8A3', 'Pacific Islander':'#EB6ACC'}

  g1 = sns.barplot(data=racial_df.sort_values('rate_of_oy', ascending=False), x='Race', y='rate_of_oy', hue='Race', ax=ax[0], palette=race_palette)
  ax[0].set_xticklabels(labels=racial_df.sort_values('rate_of_oy', ascending=False)['Race'], rotation=90, ha='left')
  ax[0].set_ylabel('Percent of Youth Pop. by Race That Are Opportunity Youth')
  ax[0].set_title('Prevelance of OY Within Race')
  racial_df_sort_prop_oy = racial_df.sort_values('proportion_of_oy', ascending=False)
  g2 = sns.barplot(data=racial_df_sort_prop_oy, x='Race', y='proportion_of_oy', hue='Race', ax=ax[1], palette=race_palette)
  ax[1].set_xticklabels(labels=racial_df_sort_prop_oy['Race'], rotation=90, ha='left')
  ax[1].set_ylabel('Percent of Representation in Opportunity Youth Pop.')
  ax[1].set_title('Who Makes Up OY in SKC')
  pass