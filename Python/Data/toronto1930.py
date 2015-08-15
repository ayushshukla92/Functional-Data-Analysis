
# coding: utf-8

# In[1]:

import pandas as pd


# In[4]:

pd.read_csv('Toronto1930.csv')


# In[5]:

data = pd.read_csv('Toronto1930.csv')


# In[6]:

data.describe()


# In[9]:

data.columns[9]


# In[10]:

meanTempDay = data[data.columns[9]]


# In[11]:

meanTempDay


# In[13]:

meanTempDay[:]


# In[19]:

meanTempDay[1:15]


# In[20]:

meanTempDay.mean()


# In[27]:

import numpy as np


# In[53]:

l = []


#  

# In[54]:

for i in xrange(24):
    l.append( (meanTempDay[15*i:15*i+15].mean() ) )


# In[55]:

l


# In[56]:

fifteenDaysMean = pd.DataFrame(l)


# In[57]:

fifteenDaysMean


# In[84]:

import matplotlib.pyplot as plt
x = np.linspace(0,23,24)
y = np.array(l)


# In[ ]:

plt.plot(x, y, 'bo', ms= 5)


# In[ ]:

plt.show()


# In[ ]:



