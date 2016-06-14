import numpy as np
from numpy import *
import time
import pandas as pd
import random
from datetime import datetime
import matplotlib.pyplot as plt

################################ Start defining functions #####################################

def genderDataframe(resultMerge,gender):
    df = pd.DataFrame(columns=resultMerge.columns)
    for i in range(0,resultMerge.shape[0]):
        if (resultMerge.ix[i,'gender']==gender):
            df.loc[len(df)] = resultMerge.loc[i,:]
    return df


def getActivelistener(resultMerge, arrayRM, df):
    listGender = []
    for i,userid in enumerate(arrayRM):
        dummyDF = pd.DataFrame(columns=resultMerge.columns)
        dummyDF = df[df['user_id']==userid]
        for i in range(0,dummyDF.shape[0]):
            s = dummyDF.ix[i,'end_timestamp']
            t = datetime.fromtimestamp(s).strftime('%m/%d/%Y %H:%M:%S')
            dummyDF.ix[i, 'end_timestamp'] = t
        dummyDF["end_timestamp"] = dummyDF["end_timestamp"].apply(lambda x: datetime.strptime(x,"%m/%d/%Y %H:%M:%S"))
        dummyDF['new_date'] = dummyDF['end_timestamp'].dt.date
        dummyDF['new_time'] = dummyDF['end_timestamp'].dt.time
        dummy = dummyDF.sort_values(['new_date', 'new_time'], ascending=[True, True]).reset_index(drop = True)
        #dummy = dummyDF.ix[pd.to_datetime(dummyDF.new_date).order().index]
        for value in range(0,dummy.shape[0]):
            if value==dummy.shape[0]:
                break
            else:
                dummylist = []
                if (dummy.ix[value,'new_date'] != dummy.ix[value+1, 'new_date']):
                    continue
                elif (dummy.ix[value,'new_date'] == dummy.ix[value+1, 'new_date']):
                    if ((dummy.ix[value,'new_time']).hour == (dummy.ix[value+1, 'new_time']).hour):
                        if ((dummy.ix[value,'new_time']).minute == (dummy.ix[value+1, 'new_time']).minute):
                            timenow = (dummy.ix[value,'new_time']).second
                            timenext = (dummy.ix[value+1,'new_time']).second
                            if ((timenext - timenow) < 30):
                                dummylist.append(1)
                listGender.append(sum(dummylist))

    return listGender

def getHist(listGender):
    data = np.array(listGender)
    bins = np.arange(data.min(), data.max()+1)
    plt.hist(data, bins = bins)

################################ End of defining functions #####################################

np.set_printoptions(precision=1, threshold=np.inf)
pd.set_option('max_columns', 80)

endSongSample = pd.read_csv("/Users/Akshita/Downloads/data_sample/end_song_sample.csv").dropna(axis  = 0, how = 'any')
userDataSample = pd.read_csv("/Users/Akshita/Downloads/data_sample/user_data_sample.csv").dropna(axis  = 0, how = 'any')

##################### Check value ranges to detect potential outliers ######################

# Remove what looks like an incorrect number for AccountAge
userDataSample = userDataSample[userDataSample['acct_age_weeks'] != -1]

################################# Merge the two datasets ###################################
resultMerge = pd.merge(endSongSample, userDataSample, how='inner', on='user_id').dropna(axis  = 0, how = 'any')
arrayRM = np.unique(resultMerge['user_id'])

######### Break the dataset into two dataframes according to their gender #########
dfFemale = genderDataframe(resultMerge, 'female')
dfMale = pd.DataFrame(resultMerge, 'male')

############### Get the number of song change under 30 sec per user pre gender ##############
listFemale = getActivelistener(resultMerge, arrayRM, dfFemale)
listMale = getActivelistener(resultMerge, arrayRM, dfMale)

################################# Get the histograms ###################################
getHist(listFemale)
getHist(listMale)