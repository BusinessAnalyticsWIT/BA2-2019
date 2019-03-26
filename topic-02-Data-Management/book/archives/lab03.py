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
print(len(subset1))

subset2 = subset1.copy()

# replacing missing data
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

#data management missing values
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

#recoding values

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

c13=subset2['USFREQMO'].value_counts(sort=True, dropna=False)
print(c13)

#lab3 step 1 add a variable
#make sure S2AQ3C1 is a number
subset2['S3AQ3C1']=pandas.to_numeric(subset2['S3AQ3C1'])


#create new secondary variable to hold number of cigarettes per month
subset2['NUMCIGMO_EST'] = subset2['USFREQMO'] * subset2['S3AQ3C1']

#make a new subset with only certain varialbes are included
subset3=subset2[['IDNUM','S3AQ3C1','USFREQMO', 'NUMCIGMO_EST']]

#display only the first 25 rows of data in the new subset
subset3.head(25)

#Step 4 regroup values
#quartile split qcut function into 4 groups
print('AGE - 4 Categories - quartiles')
subset2['AGEGROUP'] = pandas.qcut(subset2.AGE, 4, labels=['1=25%tile','2=50%tile','3=75%tile','4=100%tile'])
c14= subset2['AGEGROUP'].value_counts(sort=False, dropna=True)
print(c14)

#categorise variable based on customised splits using the cut() functions
# splits into three groups, 18-20, 21-22, and 23-25
subset2['AGEGROUP2']= pandas.cut(subset2.AGE, [17, 20, 22, 25], labels=['18-20','21-22','23-25'])
c15 = subset2['AGEGROUP2'].value_counts(sort=False, dropna=True)
print(c15)

print(pandas.crosstab(subset2['AGEGROUP2'],subset2['AGE']))

