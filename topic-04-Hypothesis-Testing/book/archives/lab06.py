# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 14:02:12 2019

@author: BMULLALLY
"""

import numpy
import pandas


nesarc_data = pandas.read_csv('nesarc_pds.csv', low_memory=False)

#SETTING MISSING SPACES in TEXT DATA
nesarc_data['CHECK321']=nesarc_data['CHECK321'].replace(' ', numpy.nan)

#setting variables you will be working with to numeric
nesarc_data['CHECK321'] = pandas.to_numeric(nesarc_data['CHECK321'], errors='ignore')
nesarc_data['S3AQ3B1'] = pandas.to_numeric(nesarc_data['S3AQ3B1'], errors='ignore')
nesarc_data['S3AQ3C1'] = pandas.to_numeric(nesarc_data['S3AQ3C1'], errors='ignore')

#subset data to young adults age 18 to 25 who have smoked in the past 12 months
sub1 = nesarc_data[(nesarc_data['AGE']>=18) & (nesarc_data['AGE']<=25) & (nesarc_data['CHECK321']==1)]

p1=len(sub1)
print(p1)


#SETTING MISSING NUMERICAL DATA
sub1['S3AQ3B1']=sub1['S3AQ3B1'].replace(9, numpy.nan)
sub1['S3AQ3C1']=sub1['S3AQ3C1'].replace(99, numpy.nan)

#recoding number of days smoked in the past month
recode1 = {1: 30, 2: 22, 3: 14, 4: 5, 5: 2.5, 6: 1}
sub1['USFREQMO']= sub1['S3AQ3B1'].map(recode1)

#converting new variable USFREQMMO to numeric
sub1['USFREQMO']= sub1['USFREQMO'].convert_objects(convert_numeric=True)

# Creating a secondary variable multiplying the days smoked/month and the number of cig/per day
sub1['NUMCIGMO_EST']=sub1['USFREQMO'] * sub1['S3AQ3C1']

sub1['NUMCIGMO_EST']= sub1['NUMCIGMO_EST'].convert_objects(convert_numeric=True)

ct1 = sub1.groupby('NUMCIGMO_EST').size()
print (ct1)