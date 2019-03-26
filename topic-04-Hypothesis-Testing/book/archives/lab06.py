# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 14:02:12 2019

@author: BMULLALLY
"""

import numpy
import pandas
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp as multi


nesarc_data = pandas.read_csv('nesarc_pds.csv', low_memory=False)

#SETTING MISSING SPACES in TEXT DATA
nesarc_data['CHECK321']=nesarc_data['CHECK321'].replace(' ', numpy.nan)
nesarc_data['S3AQ3B1'] = nesarc_data['S3AQ3B1'].replace(' ', numpy.nan)
nesarc_data['S3AQ3C1'] = nesarc_data['S3AQ3C1'].replace(' ', numpy.nan)

#setting variables you will be working with to numeric
nesarc_data['CHECK321'] = pandas.to_numeric(nesarc_data['CHECK321'])
nesarc_data['S3AQ3B1'] = pandas.to_numeric(nesarc_data['S3AQ3B1'])
nesarc_data['S3AQ3C1'] = pandas.to_numeric(nesarc_data['S3AQ3C1'])

#subset data to young adults age 18 to 25 who have smoked in the past 12 months
sub1 = nesarc_data.copy()

sub1 = sub1[(sub1['AGE']>=18) & (sub1['AGE']<=26) & (sub1['CHECK321']==1)]


#SETTING MISSING NUMERICAL DATA
sub1['S3AQ3B1']=sub1['S3AQ3B1'].replace(9, numpy.nan)
sub1['S3AQ3C1']=sub1['S3AQ3C1'].replace(99, numpy.nan)

#recoding number of days smoked in the past month
recode1 = {1: 30, 2: 22, 3: 14, 4: 5, 5: 2.5, 6: 1}
sub1['USFREQMO']= sub1['S3AQ3B1'].map(recode1)

#test that the maping took place
output = sub1[['S3AQ3B1','USFREQMO']]
print(output)

# Create a secondary variable multiplying the days smoked/month and the number of cig/per day
sub1['NUMCIGMO_EST']=sub1['USFREQMO'] * sub1['S3AQ3C1']

print(sub1['NUMCIGMO_EST'])

ct1 = sub1.groupby('NUMCIGMO_EST').size()
print (ct1)

# using OLS function for calculating the F-statistic and associated p value

model1 = smf.ols(formula='NUMCIGMO_EST ~ C(MAJORDEPLIFE)', data=sub1)
results1 = model1.fit()
print(results1.summary())

#calculate the means and standard deviations for monthly smoking for each category of MAJORDEPLIFE
print('means for numcigmo_est by major depression status')

#subset of only two variables
sub2=sub1[['NUMCIGMO_EST', 'MAJORDEPLIFE']].dropna()

#Sample size
print(len(sub2)) 


m1=sub2.groupby('MAJORDEPLIFE').mean()
print(m1)

print('standard deviations for numcigmo_est by major depression status')
sd1 = sub2.groupby('MAJORDEPLIFE').std()
print(sd1)


##ethinicity & smoking - graph delveloped in lab 4 step 4

#subset of only two variables
sub3=sub1[['NUMCIGMO_EST', 'ETHRACE2A']].dropna()

model2 = smf.ols(formula='NUMCIGMO_EST ~ C(ETHRACE2A)', data=sub3)
results2 = model2.fit()
print(results2.summary())

#calculate the means and standard deviations for monthly smoking for each category of MAJORDEPLIFE
print('means for numcigmo_est by Ethnic race')


#Sample size
#print(len(sub3)) 

#Recode variable type and categories instead of 1 to 5
sub3['ETHRACE2A'] = sub3['ETHRACE2A'].astype('category')

sub3['ETHRACE2A'] = sub3['ETHRACE2A'].cat.rename_categories(['White','Black','NatAm','Asian','Hispanic'])


m1=sub3.groupby('ETHRACE2A').mean()
print(m1)

print('standard deviations for numcigmo_est by ethnic race')
sd1 = sub3.groupby('ETHRACE2A').std()
print(sd1)

#post hoc test

mc1 = multi.MultiComparison(sub3['NUMCIGMO_EST'], sub3['ETHRACE2A'])
res1 = mc1.tukeyhsd()
print(res1.summary())

