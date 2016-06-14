import numpy as np
from numpy import *
import pandas as pd
import matplotlib.pyplot as plt


# Define functions
#**********************************************#
def AddValue(dictionary, key, value):
    dictionary[key].append(value)


np.set_printoptions(precision=1, threshold=np.inf)
pd.set_option('max_columns', 80)

endSongSample = pd.read_csv("/Users/Akshita/Downloads/data_sample/end_song_sample.csv").dropna(axis  = 0, how = 'any')
userDataSample = pd.read_csv("/Users/Akshita/Downloads/data_sample/user_data_sample.csv").dropna(axis  = 0, how = 'any')

############### Check value ranges to detect potential outliers ################
# Remove what looks like an incorrect number for AccountAge
userDataSample = userDataSample[userDataSample['acct_age_weeks'] != -1]

############################ Merge the two datasets #############################
resultMerge = pd.merge(endSongSample, userDataSample, how='inner', on='user_id').dropna(axis  = 0, how = 'any')
arrayRM = np.unique(resultMerge['user_id'])

####################### Check if each user is affiliated to a single PRODUCT STATUS ######################
dictProdStatus = {}
for i,userid in enumerate(arrayRM):
    key = userid
    dictProdStatus.setdefault(key,0)
    productStatus = (resultMerge['product'].ix[resultMerge['user_id']==userid].reset_index(drop = True)).unique()
    dictProdStatus[key] = []
    """if (len(productStatus)>1):
        print("A user has more than one product status")
        AddValue(dictProdStatus, key, productStatus[:][0])
        AddValue(dictProdStatus, key, productStatus[:][1])"""

    AddValue(dictProdStatus, key, productStatus[:])

################################ Generate age group for every user ###################################

dictUserAge = {}
for i ,userid in enumerate(arrayRM):
    #AddValue(dictUserAge, userid, 0)
    agerange = (resultMerge['age_range'].ix[resultMerge['user_id']==userid].reset_index(drop = True)).unique()
    print(type(agerange[:][0]))
    dictUserAge[userid] = agerange[:][0]

########################### Build a dataframe with age and their product status #########################
index = np.unique(dictUserAge.values())
columns = ['basic-desktop', 'free', 'premium', 'open']
dfAgevsPS = pd.DataFrame(0 , index, columns)

for i, agegroup in enumerate(index):
    print("Age group is:{0}".format(agegroup))
    for k in list(dictUserAge.keys()):
        if (dictUserAge[k]==agegroup):
            productStatus = dictProdStatus[k]
            for value in productStatus:
                dfAgevsPS.ix[agegroup, value] +=1


############## Plotting the frequency of product status for every age group in each age group ###############

fig, ax = plt.subplots()
index = np.arange(dfAgevsPS.shape[0])
bar_width = 0.2
opacity = 0.9

BD = plt.bar(index, dfAgevsPS.loc[:,'basic-desktop'], bar_width, alpha=opacity, color='b',label='basic-desktop')
free = plt.bar(index + bar_width, dfAgevsPS.loc[:,'free'], bar_width, alpha=opacity, color='r',label='free')
premium = plt.bar(index + (2*bar_width), dfAgevsPS.loc[:,'premium'], bar_width, alpha=opacity, color='y',label='premium')
open = plt.bar(index + (3*bar_width), dfAgevsPS.loc[:,'open'], bar_width, alpha=opacity, color='g',label='open')

plt.xlabel('Age-groups')
plt.ylabel('Number of users')
plt.title('Age group vs. Number of users')
plt.xticks(index + (3*bar_width), ('0-17', '18 - 24', '25 - 29', '30 - 34', '35 - 44', '45 - 54', '55+'))
plt.legend()
plt.show()