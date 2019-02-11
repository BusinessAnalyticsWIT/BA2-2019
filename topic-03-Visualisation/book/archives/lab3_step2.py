# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:34:08 2018

@author: BMULLALLY
"""

import pandas 
import numpy 

data = pandas.read_csv('addhealth_pds.csv', low_memory=False)

#convert all to number data type
data['H1GI4'] = pandas.to_numeric(data['H1GI4'])
data['H1GI6A'] = pandas.to_numeric(data['H1GI6A'])
data['H1GI6B'] = pandas.to_numeric(data['H1GI6B'])
data['H1GI6C'] = pandas.to_numeric(data['H1GI6C'])
data['H1GI6D'] = pandas.to_numeric(data['H1GI6D'])


#replace missing values for options 6 and 8
data['H1GI4'] = data['H1GI4'].replace([6,8], numpy.nan)
data['H1GI6A'] = data['H1GI6A'].replace([6,8], numpy.nan)
data['H1GI6B'] = data['H1GI6B'].replace([6,8], numpy.nan)
data['H1GI6C'] = data['H1GI6C'].replace([6,8], numpy.nan)
data['H1GI6D'] = data['H1GI6D'].replace([6,8], numpy.nan)

data['NUMETHNIC'] = data['H1GI4'] + data['H1GI6A'] + data['H1GI6B'] + data['H1GI6C'] + data['H1GI6D']

print('counts for new variable NUMETHNIC')
c1= data['NUMETHNIC'].value_counts(sort=True)
print(c1)


def ETHNICITY (row):
    if row['NUMETHNIC']>1:
        return 1
    if row['H1GI4'] ==1:
        return 2
    if row['H1GI6A'] ==1:
        return 3
    if row['H1GI6B'] ==1:
        return 4
    if row['H1GI6C']==1:
        return 5
    if row['H1GI6D']==1:
        return 6
    
data['ETHNICITY'] = data.apply(lambda row: ETHNICITY (row), axis=1)

sub2 = data[['AID', 'H1GI4','H1GI6A','H1GI6B','H1GI6C','H1GI6D','NUMETHNIC','ETHNICITY']]
a = sub2.head(n=25)
print(a)

