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
  
  # for diploma working stats
  oy_by_age_df = pd.read_csv('oy_by_age.csv')
  return full_dfs, racial_df, age_df_dict, oy_by_age_df


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

def rename_oy_by_age_df_columns(oy_by_age_df):
  oy_by_age_df.columns = ['unnamed: 0', 
                        'group', 
                        '16_18_%', 
                        '16_18_values', 
                        '19_21_%', 
                        '19_21_values', 
                        '22_24_%', 
                        '22_24_values', 
                        'totals_%', 
                        'totals_values']

def add_values_to_top_of_bars(axis_obj, axis_index):
  for p in axis_obj[axis_index].patches:
      axis_obj[axis_index].annotate("%.2f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
          ha='center', va='center', fontsize=11, color='gray', xytext=(0, 20),
          textcoords='offset points')

def plot_working_diploma_status(oy_by_age_df):
  #rename columns to be accessable
  rename_oy_by_age_df_columns(oy_by_age_df)

  # create subplot figure
  fig, axs = plt.subplots(1,3,figsize=(18,6))

  # plot 16-18 yr olds
  sns.barplot(data = oy_by_age_df, x = 'group', y='16_18_values', ax = axs[0])
  axs[0].set(ylabel='Pop. by Class for 16-18 yrs.', xlabel='Classification')
  axs[0].set_xticklabels(oy_by_age_df['group'], rotation = 45)

  # plot 19-21 yr olds
  sns.barplot(data = oy_by_age_df, x = 'group', y='19_21_values', ax = axs[1])
  axs[1].set(ylabel='Pop. by Class for 19-21 yrs.', xlabel='Classification')
  axs[1].set_xticklabels(oy_by_age_df['group'], rotation = 45)

  # plot 22-24 yr olds
  sns.barplot(data = oy_by_age_df, x = 'group', y='22_24_values', ax = axs[2])
  axs[2].set(ylabel='Pop. by Class for 22-24 yrs.', xlabel='Classification')
  axs[2].set_xticklabels(oy_by_age_df['group'], rotation = 45)

  # add pop. values to tops of bars
  add_values_to_top_of_bars(axs, 0)
  add_values_to_top_of_bars(axs, 1)
  add_values_to_top_of_bars(axs, 2)