# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 13:49:20 2024

@author: u14093767
"""


from scipy.stats import levene
import pandas as pd

# Read data from Excel sheet
data = pd.read_excel('C:/Users/u14093767/Desktop/Phenospex raw data/Maize_Combined_Day_Number.xlsx')

# Filter data to start at day 30 and end at day 80
data_filtered = data[(data['Day after planting'] >= 35) & (data['Day after planting'] <= 60)]

# Remove columns where height exceeds 1000 mm
data_filtered = data_filtered[data_filtered['Height [mm]'] <= 999]

# Perform Levene's test for homogeneity of variances
alpha = 0.05
results_levene = []

for column in data_filtered.select_dtypes(include=['float64', 'int64']).columns:
    groups = [data_filtered.loc[data_filtered['Treatment'] == treatment, column] for treatment in data_filtered['Treatment'].unique()]
    statistic, p_value = levene(*groups)
    results_levene.append({'Column': column, 'Test Statistic': statistic, 'P-value': p_value, 'Significance': 'Homogeneous' if p_value >= alpha else 'Not Homogeneous'})

# Create a DataFrame from the results
results_levene_df = pd.DataFrame(results_levene)

# Write the results to an Excel file
output_file = 'Levene_Test_Results.xlsx'
results_levene_df.to_excel(output_file, index=False)

print(f"Results saved to '{output_file}'")

