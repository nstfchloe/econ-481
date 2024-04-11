#!/usr/bin/env python
# coding: utf-8

# # Exercise 0

# In[ ]:


def github() -> str:
    return "https://github.com/nstfchloe/econ-481/blob/main/econ481HW1.ipynb"


# # Exercise 1

# In[4]:


import numpy as np
from scipy.optimize import minimize


# In[2]:


import numpy as np

def simulate_data(seed: int = 481) -> tuple:
    np.random.seed(seed)
    x_1 = np.random.normal(0, np.sqrt(2), (1000, 1))
    x_2 = np.random.normal(0, np.sqrt(2), (1000, 1))
    x_3 = np.random.normal(0, np.sqrt(2), (1000, 1))
    X = np.hstack([x_1, x_2, x_3])
    e = np.random.normal(0, 1, (1000, 1))
    y = 5 + 3*x_1 + 2*x_2 + 6*x_3 + e
    return y, X

# Call the function to generate data and print shapes to verify
y, X = simulate_data()
print("Shape of y:", y.shape)
print("Shape of X:", X.shape)


# # Exercise 2

# In[29]:


def negative_log_likelihood(beta):
    beta = beta.reshape((-1, 1))
    X_1 = np.hstack((np.ones((X.shape[0], 1)), X))
    y_pred = X_1 @ beta
        
    nll = np.sum((y - y_pred)**2)/2- 500 * np.log(2* np.pi)
    return nll


def estimate_mle(y: np.array, X: np.array) -> np.array:
   
    initial_guess = np.zeros(4)
    result = minimize(negative_log_likelihood, initial_guess, args=(), method='Nelder-Mead')
    beta_estimated = result.x
    return beta_estimated


y, X = simulate_data()  
beta_estimated = estimate_mle(y, X)
print(beta_estimated)


# # Exercise 3

# In[28]:


def negative_log_likelihood(beta):
    beta = beta.reshape((-1, 1))
    X_1 = np.hstack((np.ones((X.shape[0], 1)), X))
    y_pred = X_1 @ beta
        
    nll = np.sum((y - y_pred)**2)
    return nll


def estimate_ols(y: np.array, X: np.array) -> np.array:
   
    initial_guess = np.zeros(4)
    result = minimize(negative_log_likelihood, initial_guess, args=(), method='Nelder-Mead')
    beta_estimated = result.x
    return beta_estimated


y, X = simulate_data()  
beta_estimated = estimate_ols(y, X)
print(beta_estimated)


# In[ ]:




