#!/usr/bin/env python
# coding: utf-8

# # Exercise 0

# In[21]:


def github() -> str:
    return "https://github.com/nstfchloe/econ-481/blob/main/econ481HW1.ipynb"


# # Exercise 1

# In[16]:


import numpy
import pandas
import scipy
import matplotlib
import seaborn


# # Exercise 2

# In[17]:


def evens_and_odds(n: int) -> dict:
    evens_sum = 0
    odds_sum = 0

    for i in range(n):
        if i % 2 == 0:
            evens_sum += i
        else:
            odds_sum += i
            
    return {'evens': evens_sum, 'odds': odds_sum}


# # Exercise 3

# In[18]:


from typing import Union
from datetime import datetime

def time_diff(date_1: str, date_2: str, out: str = 'float') -> Union[str, float]:
    date_1_obj = datetime.strptime(date_1, '%Y-%m-%d')
    date_2_obj = datetime.strptime(date_2, '%Y-%m-%d')

    time_difference = abs((date_1_obj - date_2_obj).days)

    if out == 'float':
        return time_difference
    elif out == 'string':
        return f"There are {time_difference} days between the two dates"


# # Exercise 4

# In[19]:


def reverse(in_list: list) -> list:
    reversed_list = []
    for i in range(len(in_list) - 1, -1, -1):
        reversed_list.append(in_list[i])
    return reversed_list


# # Exercise 5

# In[20]:


def prob_k_heads(n: int, k: int) -> float:
    def binomial_coefficient(n, k):
        if k == 0 or k == n:
            return 1
        else:
            return binomial_coefficient(n-1, k-1) + binomial_coefficient(n-1, k)

    p_head = 0.5
    probability = binomial_coefficient(n, k) * (p_head ** k) * ((1 - p_head) ** (n - k))
    return probability


# In[ ]:





# In[ ]:




