# importing packages

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
DBNAME = 'opportunity_youth'
conn = psycopg2.connect(dbname=DBNAME)


#       import 'groomed' csv data assign to variables as dataframes
def import_and_assign():
    # df of ALL youth (age 16-24) in South King County
    ay_df = pd.read_csv('ay_df.csv')
    # df of OPPORTUNITY youth (age 16-24) in South King County
    oy_df = pd.read_csv('oy_df.csv')

    full_dfs = [ay_df, oy_df]
    # racial df
    racial_df = pd.read_csv('racial_data.csv')

    # age dfs
    ay_df_16_18 = pd.read_csv('ay_df_16_18.csv')
    ay_df_19_21 = pd.read_csv('ay_df_19_21.csv')
    ay_df_22_24 = pd.read_csv('ay_df_22_24.csv')
    oy_df_16_18 = pd.read_csv('oy_df_16_18.csv')
    oy_df_19_21 = pd.read_csv('oy_df_19_21.csv')
    oy_df_22_24 = pd.read_csv('oy_df_22_24.csv')
    age_df_dict = {'total_youth': [ay_df_16_18, ay_df_19_21, ay_df_22_24], 'opportunity_youth': [
        oy_df_16_18, oy_df_19_21, oy_df_22_24]}

    # for diploma/working stats
    oy_by_age_df = pd.read_csv('oy_by_age.csv')
    oy_by_education = pd.read_csv('oy_by_education.csv')
    oy_by_education_2016 = pd.read_csv('oy_by_education_2016.csv')

    return full_dfs, racial_df, age_df_dict, oy_by_age_df, oy_by_education, oy_by_education_2016


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
    oy_percentage_of_age_pop = [
        int(o) / int(y) for o, y in zip(oy_age_group_val_list, ay_age_group_val_list)]
    oy_percentage_of_age_pop = [x*100 for x in oy_percentage_of_age_pop]
    return ay_age_group_val_list, oy_age_group_val_list, oy_percentage_of_age_pop, age_group_strings


#       rename columns of racial_df to be camel case so they can be called
#       accessed w pandas
def rename_race_df_columns(racial_df):
    racial_df.columns = ['unnamed', 'Race',  'rate_of_oy',
                         'total_youth_pop',  'proportion_of_oy', 'oy_total']
    return racial_df


#        resize bars on graph to width 0.8 and set bars to overlap slightly
def resize_and_overlap_bars(axis):
    for patch in axis.patches:
        new_value = 0.8
        current_width = patch.get_width()
        # diff = current_width - new_value

        #  change the bar width
        patch.set_width(new_value)

        #  recenter the bar
        patch.set_x(patch.get_x() * .5)
    pass


#       rename columns from oy_by_age_df to be usable by plotting function
#       ( 2nd column title in oy_by_age_df is an empty string)
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


#       print numeric values of data on top of bars on bar plot
def add_values_to_top_of_bars(axis_obj, axis_index):
    for p in axis_obj[axis_index].patches:
        axis_obj[axis_index].annotate("%.2f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                                      ha='center', va='center', fontsize=11, color='gray', xytext=(0, 20),
                                      textcoords='offset points')


#                                     <------------------------ PLOTS ------------------------>


#       generate bar plot:
#         number of opportunity youth in SKC in 2016 vs. 2020


def plot_16_v_20(full_dfs):
    num_oy_2016 = 18817
    plt.bar(['2016', '2020'], [num_oy_2016, full_dfs[1]['pwgtp'].sum()])
    plt.title('Number of OY in SKC 2016 vs. 2020')


#       generate bar plot:
#         percent of age group representated in OY population
def plot_percent_oy_by_age(oy_percentage_of_age_pop, age_group_strings):
    plt.ylim(0, 50)
    plt.bar(age_group_strings, oy_percentage_of_age_pop)
    plt.title('Opportunity Youth {%} representation in each age group')
    plt.xlabel('Age Group')
    plt.ylabel('Percent of Age Group')


#       generate bar plots:
#         individual situation plots by age (used in plot_in_depth_age())
def age_group_bar_plot(y, x, ax, age_palette, title):
    sns.barplot(y=y, x=x, ax=ax, hue=x, palette=age_palette).set_title(
        title, fontsize=15)
    ax.get_xaxis().set_visible(False)
    for patch in ax.patches:
        patch.set_width(0.4)
        patch.set_x(patch.get_x() * 0.8)


#       generate bar plots:
#         age stats for AY & OY aswell as percent of age group
#         representated in OY population
def plot_in_depth_age(age_df_dict):
    ay_age_group_val_list, oy_age_group_val_list, oy_percentage_of_age_pop, age_group_strings = get_age_plot_reqs(
        age_df_dict)
    sns.set_style("darkgrid")
    age_palette = {'16-18': '#FF337A', '19-21': '#6F5EEB', '22-24': '#6EFFF4'}
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))

    axes[0].set_ylim(0, 35000)
    axes[1].set_ylim(0, 35000)
    axes[2].set_ylim(0, 50)

    age_group_bar_plot(oy_age_group_val_list, age_group_strings,
                       axes[0], age_palette, 'Number of Opportunity Youth by Age in South King County')
    age_group_bar_plot(ay_age_group_val_list, age_group_strings,
                       axes[1], age_palette, 'Number of Non-Opportunity Youth by Age in South King County')
    age_group_bar_plot(oy_percentage_of_age_pop, age_group_strings,
                       axes[2], age_palette, 'Opportunity Youth Percent of Pop. by Age')

    add_values_to_top_of_bars(axes, 0)
    add_values_to_top_of_bars(axes, 1)
    add_values_to_top_of_bars(axes, 2)


#       generate bar plots:
#         breakdown of AY % representation by race and breakdown of OY % representation by race
def plot_racial_representation(racial_df):
    rename_race_df_columns(racial_df)

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    race_palette = {'White': '#87FFF6', 'Hispanic': '#A6E87B', 'African American': '#FFE294', 'Asian': '#E88D7B',
                    'Two or More Races': '#DD9EFF', 'Other Race': '#A187FF', 'Native American or Alaska Native': '#7BE8A3', 'Pacific Islander': '#EB6ACC'}

    g1 = sns.barplot(data=racial_df.sort_values('rate_of_oy', ascending=False),
                     x='Race', y='rate_of_oy', hue='Race', ax=ax[1], palette=race_palette)
    # ax[0].set_xticklabels(labels=racial_df.sort_values('rate_of_oy', ascending=False)['Race'], rotation=90, ha='left')
    ax[1].get_xaxis().set_visible(False)
    ax[1].set_ylabel(
        'Percent of Youth Pop. by Race That Are Opportunity Youth')
    ax[1].set_title('Prevelance of OY Within Race')

    g2 = sns.barplot(data=racial_df.sort_values('proportion_of_oy', ascending=False),
                     x='Race', y='proportion_of_oy', hue='Race', ax=ax[0], palette=race_palette)
    # ax[1].set_xticklabels(labels=racial_df_sort_prop_oy['Race'], rotation=90, ha='left')
    ax[0].get_xaxis().set_visible(False)
    ax[0].set_ylabel('Percent of Representation in Opportunity Youth Pop.')
    ax[0].set_title('Who Makes Up OY in SKC')

    resize_and_overlap_bars(ax[0])
    resize_and_overlap_bars(ax[1])


#       generate plot:
#         status of diploma/GED and work status by age group
def plot_working_diploma_status(oy_by_age_df):
    # rename columns to be accessable
    rename_oy_by_age_df_columns(oy_by_age_df)

    education_palette = {'Total Population': '#FFCF4E', 'Opportunity Youth': '#E8483A',
                         'Working Without Diploma': '#8B4DFF', 'Not an Opportunity Youth': '#3AE1E8'}

    # create subplot figure
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))

    # plot 16-18 yr olds
    sns.barplot(data=oy_by_age_df, x='group', y='16_18_values',
                ax=axs[0], hue='group', palette=education_palette)
    axs[0].set(ylabel='Pop. by Class for 16-18 yrs.', xlabel='Classification')
    axs[0].set_xticklabels(oy_by_age_df['group'], rotation=45)
    axs[0].get_xaxis().set_visible(False)
    # plot 19-21 yr olds
    sns.barplot(data=oy_by_age_df, x='group', y='19_21_values',
                ax=axs[1], hue='group', palette=education_palette)
    axs[1].set(ylabel='Pop. by Class for 19-21 yrs.', xlabel='Classification')
    axs[1].set_xticklabels(oy_by_age_df['group'], rotation=45)
    axs[1].get_xaxis().set_visible(False)
    # plot 22-24 yr olds
    sns.barplot(data=oy_by_age_df, x='group', y='22_24_values',
                ax=axs[2], hue='group', palette=education_palette)
    axs[2].set(ylabel='Pop. by Class for 22-24 yrs.', xlabel='Classification')
    axs[2].set_xticklabels(oy_by_age_df['group'], rotation=45)
    axs[2].get_xaxis().set_visible(False)
    for x in axs:
        for patch in x.patches:
            patch.set_width(0.4)
            patch.set_x(patch.get_x() * 0.8)

    # add pop. values to tops of bars
    add_values_to_top_of_bars(axs, 0)
    add_values_to_top_of_bars(axs, 1)
    add_values_to_top_of_bars(axs, 2)


#       generate plot:
#         plot breakdown of education levels within opportunity youth in SKC
def plot_oy_education_breakdown_2016(oy_by_education_2016):
    rename_oy_by_age_df_columns(oy_by_education_2016)
    fig, ax = plt.subplots(1, 3, figsize=(20, 6))

    education_palette = {'No Diploma': '#FF7764',
                         'HS or GED': '#ADD3FF',
                         'Some College, No Degree': '#C27AEB',
                         'College Degree (associates+)': '#EBCB8A'}

    sns.barplot(data=oy_by_education_2016[1:], x='group', y='16_18_values',
                hue='group', ax=ax[0], palette=education_palette)
    sns.barplot(data=oy_by_education_2016[1:], x='group', y='19_21_values',
                hue='group', ax=ax[1], palette=education_palette)
    sns.barplot(data=oy_by_education_2016[1:], x='group', y='22_24_values',
                hue='group', ax=ax[2], palette=education_palette)
    ax[0].set_ylim(0, 4000)
    ax[1].set_ylim(0, 4000)
    ax[2].set_ylim(0, 4000)
    ax[0].get_xaxis().set_visible(False)
    ax[1].get_xaxis().set_visible(False)
    ax[2].get_xaxis().set_visible(False)
    for x in ax:
        for patch in x.patches:
            patch.set_width(0.4)
            patch.set_x(patch.get_x() * 0.8)

    add_values_to_top_of_bars(ax, 0)
    add_values_to_top_of_bars(ax, 1)
    add_values_to_top_of_bars(ax, 2)
    pass

#       generate plot:
#         plot breakdown of education levels within opportunity youth in SKC in 2020


def plot_oy_education_breakdown_2020(oy_by_education):
    rename_oy_by_age_df_columns(oy_by_education)
    fig, ax = plt.subplots(1, 3, figsize=(20, 6))

    education_palette = {'No Diploma': '#FF7764',
                         'HS or GED': '#ADD3FF',
                         'Some College, No Degree': '#C27AEB',
                         'College Degree (associates+)': '#EBCB8A'}

    sns.barplot(data=oy_by_education[1:], x='group', y='16_18_values',
                hue='group', ax=ax[0], palette=education_palette)
    sns.barplot(data=oy_by_education[1:], x='group', y='19_21_values',
                hue='group', ax=ax[1], palette=education_palette)
    sns.barplot(data=oy_by_education[1:], x='group', y='22_24_values',
                hue='group', ax=ax[2], palette=education_palette)
    ax[0].set_ylim(0, 4000)
    ax[1].set_ylim(0, 4000)
    ax[2].set_ylim(0, 4000)
    ax[0].get_xaxis().set_visible(False)
    ax[1].get_xaxis().set_visible(False)
    ax[2].get_xaxis().set_visible(False)
    for x in ax:
        for patch in x.patches:
            patch.set_width(0.4)
            patch.set_x(patch.get_x() * 0.8)

    add_values_to_top_of_bars(ax, 0)
    add_values_to_top_of_bars(ax, 1)
    add_values_to_top_of_bars(ax, 2)
    pass
