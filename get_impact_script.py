#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 

def main_script(history_csv_name='gorongosa_purchase_history.csv', titles_csv_name='Gorongosa_Titles_V2.csv', output_name='total_impact_csv'):
    history, titles = read_data(history_csv_name, titles_csv_name)
    history_2 = clean_and_merge_data(history, titles)
    impact = get_impact(history_2)
    impact.to_csv(output_name)
    return 

def multiply_cols_by_ref_col(df, ref_col, col_list):
    for colname in col_list:
        df.loc[:, colname] = df[colname]*df[ref_col]
    return df

def read_data(history_csv_name, titles_csv_name):
    history = pd.read_csv(history_csv_name, header=1)
    titles = pd.read_csv(titles_csv_name)
    titles = titles[['Active_Product','Include_Quant','Line item title','Correct_Title','Girls ','Wildlife','Trees']]
    return history, titles

def clean_and_merge_data(history, titles):
    history_2 = history[['Customer email','Customer first name','Customer last name','Line item title','Total quantity']].merge(titles, on=['Line item title'], how='left')
    history_2 = history_2.loc[history_2.Include_Quant==1, :]
    return history_2

def get_impact(history_2):
    history_3 = multiply_cols_by_ref_col(history_2, 'Total quantity', ['Girls ','Trees','Wildlife'])
    impact = history_3.groupby(['Customer email','Customer first name','Customer last name']).agg({'Girls ':'sum','Wildlife':'sum','Trees':'sum'}).reset_index()
    return impact


# In[ ]:




