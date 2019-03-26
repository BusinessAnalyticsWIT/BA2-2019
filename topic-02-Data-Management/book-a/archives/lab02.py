# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas
import numpy

#load dataset from the csv file in the dataframe called nesarc_data
nesarc_data = pandas.read_csv('nesarc_pds.csv',low_memory=False)

#convert spaces to NAN
nesarc_data['CHECK321']=nesarc_data['CHECK321'].replace(' ', numpy.nan)

#converting strings to numeric data for better output

nesarc_data['TAB12MDX'] = pandas.to_numeric(nesarc_data['TAB12MDX'],errors='ignore')
nesarc_data['CHECK321'] = pandas.to_numeric(nesarc_data['CHECK321'],errors='ignore')
nesarc_data['S3AQ3B1'] = pandas.to_numeric(nesarc_data['S3AQ3B1'], errors='ignore')
nesarc_data['S3AQ3C1'] = pandas.to_numeric(nesarc_data['S3AQ3C1'], errors='ignore')

# restrict to those observations that are between 18 and 25 and smoke now
subset1 = nesarc_data[(nesarc_data['AGE']>=18) & (nesarc_data['AGE']<=25) & (nesarc_data['CHECK321']==1)]


print('counts for AGE ')
c1= subset1['AGE'].value_counts(sort=True)
print (c1)

print('percentages for AGE ')
c2= subset1["AGE"].value_counts(sort=True, normalize=True)
print (c2)


subset2 = subset1.copy()

#step 2 replacing missing data
#counts for S3AQ3B1
print('counts for S3AQ3B1 - usual frequency when smoked cigarettes')
c7= subset1['S3AQ3B1'].value_counts(sort=True)
print (c7)


#ensure the variable is number data type first
subset2['S3AQ3B1']=pandas.to_numeric(subset2['S3AQ3B1'])
#replace the value 9 in S3AQ3B1 with Nan to signify missing data

subset2['S3AQ3B1']=subset2['S3AQ3B1'].replace(9, numpy.NaN)

print((subset2['S3AQ3B1']==9).sum())
print(subset2['S3AQ3B1'].isnull().sum())

#counts for S3AQ3B1 after set to Nan
print(subset2.describe())
print('counts for S3AQ3B1 - usual frequency when smoked cigarettes')
c8= subset2['S3AQ3B1'].value_counts(sort=True, dropna=False)
print (c8)

#step 3 data management missing values
subset2['S2AQ3']=pandas.to_numeric(subset2['S2AQ3'])

c9=subset2['S2AQ3'].value_counts(sort=True, dropna=False)
print(c9)


c10=subset2['S2AQ8A'].value_counts(sort=True, dropna=False)
print(c10)

print((subset2['S2AQ8A']=="").sum())
print((subset2['S2AQ8A'].isnull()).sum())
print((subset2['S2AQ8A']==" ").sum())

subset2['S2AQ8A']=subset2['S2AQ8A'].replace(' ', numpy.NaN)

print(subset2['S2AQ8A'].isnull().sum())

subset2.shape
subset2.isnull().sum()

subset2.loc[(subset2['S2AQ3']!=9) & (subset2['S2AQ8A'].isnull()),'S2AQ8A']=11


print((subset2['S2AQ8A']==11).sum())

#step 4, recoding values

#first create the dictionary to recode
recode1= {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}

#next use the map funciton to replace values using the recode dictionary
subset2['USFREQ'] = subset2['S3AQ3B1'].map(recode1)

#Now recode to a quantitative value based on an estimate of how many times per month each person smokes

recode2 = {1: 30, 2: 22, 3: 14, 4: 5, 5: 2.5, 6: 1}

subset2['USFREQMO'] = subset2['S3AQ3B1'].map(recode2)


c11=subset2['S3AQ3B1'].value_counts(sort=True, dropna=False)
print(c11)

c12=subset2['USFREQ'].value_counts(sort=True, dropna=False)
print(c12)

print('counts for USFREQMO')
c13=subset2['USFREQMO'].value_counts(sort=True, dropna=False)
print(c13)

print('percentages for USFREQMO')
c14=subset2['USFREQMO'].value_counts(sort=True, normalize=True)
print(c14)

