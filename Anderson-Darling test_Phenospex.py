# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 16:31:49 2024

@author: u14093767
"""

import pandas as pd
from scipy.stats import anderson

# Read data from Excel sheet
data = pd.read_excel('C:/Users/u14093767/Desktop/Phenospex raw data/Maize_Combined_Day_Number.xlsx')

# Filter data to start at day 30 and end at day 80
data_filtered = data[(data['Day after planting'] >= 35) & (data['Day after planting'] <= 60)]

# Remove columns where height exceeds 1000 mm
data_filtered = data_filtered[data_filtered['Height [mm]'] <= 999]

# Exclude non-numeric columns
numeric_columns = data_filtered.select_dtypes(include=['float64', 'int64']).columns

# Perform Anderson-Darling test for normality on each numeric column
alpha = 0.05

for column in numeric_columns:
    result = anderson(data_filtered[column])
    print(f"Anderson-Darling test for normality on column 'Digital biomass [mm³]':")
    print(f"Test Statistic: {result.statistic}")
    print(f"Critical Values: {result.critical_values}")
    print(f"Significance Levels: {result.significance_level}")
    print(f"Is Normal: {result.statistic < result.significance_level[0]}")
    print()
