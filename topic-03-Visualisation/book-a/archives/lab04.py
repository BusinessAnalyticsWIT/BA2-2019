# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 10:06:18 2018

@author: BMULLALLY
"""

import pandas
import numpy
import seaborn
import matplotlib.pyplot as plt

#load dataset from the csv file in the dataframe called nesarc_data
nesarc_data = pandas.read_csv('nesarc_pds.csv',low_memory=False)

#set PANDAS to show all columns in Data frame
pandas.set_option('display.max_columns', None)

#set PANDAS to show all rows in Data frame
pandas.set_option('display.max_rows', None)

#converting strings to numeric data for better output

nesarc_data['TAB12MDX'] = pandas.to_numeric(nesarc_data['TAB12MDX'],errors='ignore')
nesarc_data['CHECK321'] = pandas.to_numeric(nesarc_data['CHECK321'],errors='ignore')
nesarc_data['S3AQ3B1'] = pandas.to_numeric(nesarc_data['S3AQ3B1'], errors='ignore')
nesarc_data['S3AQ3C1'] = pandas.to_numeric(nesarc_data['S3AQ3C1'], errors='ignore')

# restrict to those observations that are between 18 and 25 and smoke now
subset1 = nesarc_data[(nesarc_data['AGE']>=18) & (nesarc_data['AGE']<=25) & (nesarc_data['CHECK321']=='1')]

subset2 = subset1.copy()

#ensure the variable is number data type first
subset2['S3AQ3B1']=pandas.to_numeric(subset2['S3AQ3B1'])
#replace the value 9 in S3AQ3B1 with Nan to signify missing data

subset2['S3AQ3B1']=subset2['S3AQ3B1'].replace(9, numpy.NaN)

#first create the dictionary to recode
recode1= {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}

#next use the map funciton to replace values using the recode dictionary
subset2['USFREQ'] = subset2['S3AQ3B1'].map(recode1)

#Now recode to a quantitative value based on an estimate of how many times per month each person smokes

recode2 = {1: 30, 2: 22, 3: 14, 4: 5, 5: 2.5, 6: 1}

subset2['USFREQMO'] = subset2['S3AQ3B1'].map(recode2)

#lab6 step 1 add a variable
#make sure S2AQ3C1 is a number
subset2['S3AQ3C1']=pandas.to_numeric(subset2['S3AQ3C1'])

subset2['S3AQ3C1']=subset2['S3AQ3C1'].replace(99, numpy.NaN)

#create new secondary variable to hold number of cigarettes per month
subset2['NUMCIGMO_EST'] = subset2['USFREQMO'] * subset2['S3AQ3C1']

#make a new subset with only certain varialbes are included
subset3=subset2[['IDNUM','S3AQ3C1','USFREQMO', 'NUMCIGMO_EST']]

#display only the first 25 rows of data in the new subset
subset3.head(25)

#LAB 07 GRAPHING

#counts for TAB12MDX
print('count of TAB12MDX')
c1 = subset2.groupby('TAB12MDX').size()
print(c1)
print('same count different function used')
c2 = subset2['TAB12MDX'].value_counts(sort=False, dropna=True)
print(c2)

#percentages for TAB12MDX
print('percentages of counts')
p1 = subset2.groupby('TAB12MDX').size() * 100 /len(nesarc_data)
print(p1)

#counts for NUMCIGMO_EST
print('count of NUMCIGMO_EST')
c3 = subset2.groupby('NUMCIGMO_EST').size()
print(c3)
print('same count different function used')
c4 = subset2['NUMCIGMO_EST'].value_counts(sort=False, dropna=True)
print(c4)

#percentages for NUMCIGMO_EST
print('percentages of counts')
p2 = subset2.groupby('NUMCIGMO_EST').size() * 100 /len(nesarc_data)
print(p2)


#univariate graphing
bc1 = seaborn.countplot(x='TAB12MDX',data=subset2)
plt.xlabel('Nicotine Dependence past 12 months')
plt.title('Nicotine Dependence in the past 12 months among young adult smokers in the Nesarc study')


bc2 = seaborn.distplot(subset2['NUMCIGMO_EST'].dropna(),kde=False)
plt.xlabel('Number of cigarettes per month')
plt.title('Estimated number of cigarettes per month among young adult smokers in the Nesarc study')

#step 2 Lab7
#categorise variable based on customised splits using the cut() function
# splits into 6 groups, 1-200, 200-400, 400-600, 600-800, 800-1000, 1000-4000
print('Group the variable NUMCIGMO_EST into bins')
subset2['NUMCIGMO_EST_BINS'] = pandas.cut(subset2.NUMCIGMO_EST, [0,200,400,600,800,1000,4000], labels=['1-200','200-400','400-600','600-800','800-1000','1000-4000'])
c4 = subset2['NUMCIGMO_EST_BINS'].value_counts(sort=False,dropna=True)
print(c4)

bc3= seaborn.countplot(x='NUMCIGMO_EST_BINS', data=subset2)
plt.xlabel('Nicotine Dependence past 12 months by number of cigarettes')
plt.title('Nicotine Dependnce among young adults')


print('describe number of cigarettes smoked per month')
desc1 = subset2['NUMCIGMO_EST'].describe()
print(desc1)

print('mean')
mean1 = subset2['NUMCIGMO_EST'].mean()
print(mean1)

print('std deviation')
std1 = subset2['NUMCIGMO_EST'].std()
print(std1)

print('min')
min1 = subset2['NUMCIGMO_EST'].min()
print(min1)

print('max')
max1 = subset2['NUMCIGMO_EST'].max()
print(max1)

print('median')
median1 = subset2['NUMCIGMO_EST'].median()
print(median1)

print('mode')
mode1 = subset2['NUMCIGMO_EST'].mode()
print(mode1)

subset2['PACKSPERMONTH'] = subset2['NUMCIGMO_EST'] / 20

c5 = subset2.groupby('PACKSPERMONTH').size()
print(c5)
