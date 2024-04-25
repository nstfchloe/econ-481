#!/usr/bin/env python
# coding: utf-8

# # Exercise 0

# In[19]:


def github() -> str:
    return "https://github.com/nstfchloe/econ-481/blob/main/econ481HW4.ipynb"


# # Exercise 1

# In[25]:


import pandas as pd

def load_data() -> pd.DataFrame:
    url = 'https://lukashager.netlify.app/econ-481/data/TSLA.csv'
    df = pd.read_csv(url)

    return df


# # Exercise 2

# In[26]:


import pandas as pd
import matplotlib.pyplot as plt

def plot_close(df: pd.DataFrame, start: str = '2010-06-29', end: str = '2024-04-15') -> None:
    df['Date'] = pd.to_datetime(df['Date'])
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)
    
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_df['Date'], filtered_df['Close'], color='blue', linewidth=2)
    
    plt.title(f'Tesla stock closing price ({start} to {end})')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.grid(True)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()



# # Exercise 3

# In[27]:


import pandas as pd
import statsmodels.api as sm

def autoregress(df: pd.DataFrame) -> float:
    df['Delta_Close'] = df['Close'].diff()
    df = df.dropna()
    X = df['Delta_Close'].shift(1).iloc[1:]
    y = df['Delta_Close'].iloc[1:]
    model = sm.OLS(y, X, hasconst=False).fit(cov_type='HC1')
    t_stat = model.tvalues.iloc[0]
    return t_stat


# # Exercise 4

# In[28]:


import pandas as pd
import statsmodels.api as sm

def autoregress_logit(df: pd.DataFrame) -> float:
    df = df.copy()
    df['Delta_Close'] = df['Close'].diff()
    df = df.dropna()
    X = df['Delta_Close'].shift(1).iloc[1:]
    df.loc[:, 'Delta_Positive'] = (df['Delta_Close'] > 0).astype(int)
    y = df['Delta_Positive'].iloc[1:]
    
    model = sm.Logit(y, X).fit(disp=0)
    t_stat = model.tvalues.iloc[0]
    
    return t_stat



# # Exericise 5

# In[29]:


import pandas as pd
import matplotlib.pyplot as plt

def plot_delta(df: pd.DataFrame) -> None:
    df['Delta_Close'] = df['Close'].diff()
    plt.figure(figsize=(10, 5))
    plt.plot(df['Delta_Close'], label='Day-to-Day Change in Closing Price')
    plt.title('Day-to-Day Changes in Closing Price')
    plt.xlabel('Date')
    plt.ylabel('Change in Closing Price')
    plt.legend()
    plt.grid(True)
    plt.show()


# In[ ]:




