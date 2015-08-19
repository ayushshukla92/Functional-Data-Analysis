
# coding: utf-8

# In[1]:

import pandas as pd


# In[2]:

filename = 'Toronto2013.csv'


# In[3]:

pd.read_csv('Toronto2013.csv')


# In[4]:

data = pd.read_csv('Toronto2013.csv')


# In[5]:

data


# In[8]:

data.columns[9]


# In[9]:

meanTempDay = data[data.columns[9]]


# In[10]:

meanTempDay


# In[11]:

meanTempDay[:]


# In[12]:

meanTempDay[1:15]


# In[13]:

meanTempDay.mean()


# In[14]:

import numpy as np


# In[15]:

l = []


#  

# In[16]:

for i in xrange(24):
    l.append( (meanTempDay[15*i:15*i+15].mean() ) )


# In[17]:

l


# In[18]:

fifteenDaysMean = pd.DataFrame(l)


# In[19]:

fifteenDaysMean


# In[36]:

import matplotlib.pyplot as plt
x = np.linspace(0,23,24)
y = np.array(l)


# In[37]:

plt.plot(x, y, 'ro', ms= 5)
plt.xlabel('15 days mean')
plt.ylabel('temperature')
plt.title(filename)


# In[38]:

meanTempDay.mean()


# In[40]:

from scipy.interpolate import UnivariateSpline
spl = UnivariateSpline(x, y)
xs = np.linspace(0, 23, 1000)
plt.plot(xs, spl(xs), 'g', lw=3)




plt.text(1, meanTempDay.max()-7,'mu = '+ str( round(meanTempDay.mean(),2) ), horizontalalignment='left',
     verticalalignment='center')
plt.text(1, meanTempDay.max()-8.5,'sigma = '+ str( round(meanTempDay.std(),2) ), horizontalalignment='left',
     verticalalignment='center')
plt.show()



