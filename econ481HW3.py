#!/usr/bin/env python
# coding: utf-8

# # Exercise 0

# In[14]:


def github() -> str:
    return "https://github.com/nstfchloe/econ-481/blob/main/econ481HW3.ipynb"


# # Exercise 1

# In[15]:


import pandas as pd

def import_yearly_data(years: list) -> pd.DataFrame:
    data_frames = []
    
    for year in years:
        url = f"https://lukashager.netlify.app/econ-481/data/ghgp_data_{year}.xlsx"
        df = pd.read_excel(url, sheet_name='Direct Emitters', skiprows=3, header=0)
        df['year'] = year
        data_frames.append(df)
    
    concatenated_data = pd.concat(data_frames, ignore_index=True)
    
    return concatenated_data


# # Exercise 2

# In[16]:


def import_parent_companies(years: list) -> pd.DataFrame:
    data_frames = []
    
    for year in years:
        url = f"https://lukashager.netlify.app/econ-481/data/ghgp_data_parent_company_09_2023.xlsb"
        all_sheets = pd.read_excel(url, sheet_name=None)
        
        for sheet_name, df in all_sheets.items():
            if sheet_name == str(year):
                df['year'] = year
                df = df.dropna(how='all')
                data_frames.append(df)
    
    concatenated_data = pd.concat(data_frames, ignore_index=True)
    
    return concatenated_data


# # Excercise 3

# In[17]:


def n_null(df: pd.DataFrame, col: str) -> int:
    null_count = df[col].isnull().sum()
    
    return null_count


# # Exercise 4

# In[18]:


def clean_data(emissions_data: pd.DataFrame, parent_data: pd.DataFrame) -> pd.DataFrame:
    emissions_data['year'] = emissions_data['year'].astype(int)
    parent_data['year'] = parent_data['year'].astype(int)

    merged_data = pd.merge(emissions_data, parent_data, 
                           left_on=['year', 'Facility Id'], 
                           right_on=['year', 'GHGRP FACILITY ID'], 
                           how='left')

    subset_columns = [
        'Facility Id', 'year', 'State', 'Industry Type (sectors)', 'Total reported direct emissions', 'PARENT CO. STATE', 'PARENT CO. PERCENT OWNERSHIP'
    ]
    
    cleaned_data = merged_data[subset_columns]
    cleaned_data.columns = cleaned_data.columns.str.lower()

    return cleaned_data



# # Exercise 5

# In[19]:


def aggregate_emissions(df: pd.DataFrame, group_vars: list) -> pd.DataFrame:
    agg_vars = {
        'total reported direct emissions': ['min', 'median', 'mean', 'max'],
        'parent co. percent ownership': ['min', 'median', 'mean', 'max']
    }
    
    aggregated_data = df.groupby(group_vars).agg(agg_vars)
    sorted_data = aggregated_data.sort_values(by=('total reported direct emissions', 'mean'), ascending=False)
    
    return sorted_data


# In[ ]:





# In[ ]:




