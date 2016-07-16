import numpy as np
from numpy import *
import pandas as pd
import matplotlib.pyplot as plt

np.set_printoptions(precision=1, threshold=np.inf)
pd.set_option('max_columns', 80)

def getList(features, dataframe):
    Array = np.unique(dataframe[features])
    dictFeature = {}
    for i,feat in enumerate(Array):
        valuesFeature = sum(dataframe[features]==feat)
        dictFeature[feat] = valuesFeature
    return dictFeature

def sampleParameters(dataset, genderString, parameterString):
    dataset = dataset[dataset['gender'] == genderString]
    n = dataset.shape[0]
    x = sum(dataset[parameterString])
    sigma = np.std(dataset[parameterString], ddof=1)
    xbar = x/n
    return xbar, sigma, n

def zStatistic(xbar1, xbar2, sigma1, sigma2, n1, n2):
    num = (xbar1-xbar2)
    den = sqrt(((sigma1**2)/n1)+((sigma2**2)/n2))
    return num/den

endSongSample = pd.read_csv("/home/rcf-proj2/akr/akshitar/Apriori/end_song_sample.csv").dropna(axis  = 0, how = 'any')
userDataSample = pd.read_csv("/home/rcf-proj2/akr/akshitar/Apriori/user_data_sample.csv").dropna(axis  = 0, how = 'any')

############### Check value ranges to detect potential outliers ################
dictCountry = getList('country',userDataSample)
dictGender = getList('gender', userDataSample)
dictContext = getList('context', endSongSample)
dictProduct = getList('product' , endSongSample)
#print(dictProduct)
# Remove what looks like an incorrect number for AccountAge
userDataSample = userDataSample[userDataSample['acct_age_weeks'] != -1]

############################ Merge the two datasets #############################
resultMerge = pd.merge(endSongSample, userDataSample, how='inner', on='user_id').dropna(axis  = 0, how = 'any')

################# Check if unique user id's in both sets match ##################
arrayRM = np.unique(resultMerge['user_id'])
arrayESS = np.unique(endSongSample['user_id'])
arrayUDS = np.unique(userDataSample['user_id'])

mask = np.in1d(arrayESS, arrayUDS)

########### Determine whether male and female listeners are significantly different in their overall listening
# (in terms of the count of track listens, or in terms of the total time spent listening) ####################
######################################## Find mean ####################################
xbarFem, sigmaFem, nFem = sampleParameters(resultMerge, 'female', 'ms_played')
xbarMale, sigmaMale, nMale = sampleParameters(resultMerge, 'male', 'ms_played')
statistic = zStatistic(xbarMale, xbarFem, sigmaMale, sigmaFem, nMale, nFem)
print(statistic)
print(xbarMale - xbarFem)