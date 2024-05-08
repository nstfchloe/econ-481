#!/usr/bin/env python
# coding: utf-8

# # Exercise 0

# In[ ]:


def github() -> str:
    return "https://github.com/nstfchloe/econ-481/blob/main/econ481HW5.ipynb"


# # Exercise 1

# In[2]:


import requests
from bs4 import BeautifulSoup

def scrape_code(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    code_blocks = soup.find_all('code')
    python_code = []
    for block in code_blocks:
        lines = block.get_text().split('\n')
        filtered_lines = [line for line in lines if not line.strip().startswith('%')]
        python_code.append('\n'.join(filtered_lines))
    return '\n\n'.join(python_code)


# In[ ]:




