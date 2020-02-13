# Goal

The goal of this project was to follow up on the 2016 report of Opportunity Youth in Southern King County. Opportunity Youth are defined as people aging between 16-24 who are neither working, nor enrolled in school.

# Decyphering and Filtering the Data

The first hurdle in this project was decyphering what on Earth we were looking at. After reviewing the documentation in the resources folder, it became apparent that we were looking at census data for Washington State. Knowing our objective was to analyze information concering Southern King County, we needed to discover how to filter our data to include only the rows pertaining to that region. But what is "Southern" King County, you might ask. The answer to that question came from the following url -

https://www.kingcounty.gov/depts/health/data/community-health-indicators/definitions.aspx

Upon discovering the definition of Southern King County, and after revieiwng the puma_names_2010 table, we were able to reduce our data to entries in the puma_2017 table where the PUMA column was between 11610 and 11615.

Having filtered our data to the appropriate region, it was now time to find our youth.

# Finding and Categorizing our Youth

The focus of the study is on youth between the ages of 16 and 24, so our first demographic filter was based on the 'agep' category, eliminating all entries outside of that range. The resulting data was saved as the ay_df dataframe for future calculations.

After filtering based on age, we then needed to create a filter defining our Opportunity Youth category. To that end, we found 2 categories in the Data Dictionary that allowed us to perform this filtration: 'esr' for filtering based on employment status, and 'sch' for filtering based on educational enrollment status. We set the filter for 'esr' to NOT EQUAL to '4' or '1', thereby eliminating the youth who were working, while the filter for 'sch' was set EQUAL to '1', thereby including ONLY youth who had not attended school in the previous 3 months. 

At this point, we had successfully broken our raw data into the All Youth dataframe (saved as ay_df) and the Opportunity Youth dataframe (oy_df).

We also needed a unique category for youth who were working (so not opportunity youth), but who also hadn't acheived a high school education or GED equivalent. We ended up filtering based on those who WERE employed ('esr' EQUAL to '1' or '4'), and had NOT ACQUIRED a diploma or ged ('schl' BETWEEN '01' and '15'). We assumed this subcategory was intended to find youth who were at risk of becoming Opportunity Youth, and the dataframe was thus named Risk Youth (ry_df).

Now that we had all 3 categories of youth, we needed to perform our data analysis.

# Data Analysis

The study further divided youth based on age brackets 16-18, 19-21, and 22-24, thus we did the same, resulting in the df_START AGE_END AGE schema (e.g. ay_df_16_18 represents ALL youth from ages 16 to 18).

After having subdivided our youth dataframes, we performed the necessary computations by summing the 'pwgtp' column in the relevant dataframes (which is an applied weight to that particular entry, so 1 entry with a 'pwgtp' of 45 essentially counts as 45 people). The Census data is distributed in this manner because it's easier to work with the data set and drastically reduces the file size of the dataset. So for example, calculating the percentage of  Opportunity Youth in the 16-18 age bracket, we would perform the following aciton: 

sum(oy_df_16_18['pwgtp']) / sum(ay_df_16_18['pwgtp']). 

This operation takes the total number of Opportunity Youth in the 16-18 category and divides it by the total number of All Youth in the 16-18 category, thereby giving us the ratio of OY to AY in a given subset of data.

The final tables can be found in the Final jupyter notebook in the Notebooks/Report folder. These tables include analysis of each subcategory of Opportunity Youth by age bracket, education level, as well as race.

Although race was not a required category for analysis, we found the results interesting.

# Findings

Although our data analysis produced slightly different values, we ultimately found the same patterns as the 2016 study.

Namely, the percentage of Opportunity Youth increases as the population gets older (although with a slight drop from 19-21 to 22-24, presumably because of a lag in educational achievement and active employment). This pattern is to be expected because as age goes beyond 18, more youth are no longer in state mandated high school. 

Additionaly, and more interestingly, there is a clear relationship between race and prevalence of Opportunity Youth within that demographic. For example, although white youth make up the majority of All Youth, there is only an 11% rate of Opportunity Youth within the white population. This is contrasted by the near 40% Opportunity Youth rate of the native american population. Although this is the most extreme example, this pattern repeats itself in other minority groups as well.

It should be noted as well, that even though Hispanic is listed as a race by the 2016 study, it is not in fact categorized as a race by the Census. This resulted in a 120% total when adding up the proporton of Opportunity Youth by race. This has been noted in our presentation. 

# Further Research

Our findings, while interesting, are limited by the definitions we chose when defining the various demographics of interest. It is quite possible the 2016 study used different data filters when determining how to perform their analysis, and since we don't have access to their definitions, our results remain inconclusive.

It would be interesting to go back and perform the same analysis based on the same filters used in the 2016 study.