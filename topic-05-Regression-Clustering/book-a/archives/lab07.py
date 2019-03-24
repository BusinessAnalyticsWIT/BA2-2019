# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 11:40:16 2018

@author: Brenda
"""

import pandas
import numpy
import statsmodels.api as sm
import statsmodels.formula.api as smf

#load dataset from the csv file in the dataframe called nesarc_data
gapminder_data = pandas.read_csv('gapminder.csv',low_memory=False)

#set PANDAS to show all columns in Data frame
pandas.set_option('display.max_columns', None)

#set PANDAS to show all rows in Data frame
pandas.set_option('display.max_rows', None)

#replace blanks with Nan
gapminder_data['internetuserate']=gapminder_data['internetuserate'].replace(" ", numpy.NaN)
gapminder_data['urbanrate']=gapminder_data['urbanrate'].replace(" ", numpy.NaN)


#numeric variables that are read into python from the csv file as strings (objects)
#with empty cells should be converted back to numeric format using convert_objects function
gapminder_data['internetuserate'] = pandas.to_numeric(gapminder_data['internetuserate'])
gapminder_data['urbanrate'] = pandas.to_numeric(gapminder_data['urbanrate'])


#regression for association between urbandrate (explanatory, numerical) and internet use rate (response, numerical)
print('OLS regression model for the association between urbanrate and internet use rate')
reg1 = smf.ols('internetuserate ~ urbanrate',data=gapminder_data).fit()
print(reg1.summary())






