# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 12:35:46 2024

@author: u14093767
"""

import pandas as pd
from scipy.stats import kruskal, mannwhitneyu

# Read data from Excel sheet
data = pd.read_excel('C:/Users/u14093767/Desktop/Phenospex raw data/Maize_Combined_Day_Number.xlsx')

# Filter data to start at day 30 and end at day 80
data_filtered = data[(data['Day after planting'] >= 35) & (data['Day after planting'] <= 60)]

# Remove columns where height exceeds 1000 mm
data_filtered = data_filtered[data_filtered['Height [mm]'] <= 999]

# Perform Kruskal-Wallis test for each numeric column
alpha = 0.05
results = []

for column in data_filtered.select_dtypes(include=['float64', 'int64']).columns:
    groups = [data_filtered.loc[data_filtered['Treatment'] == treatment, column] for treatment in data_filtered['Treatment'].unique()]
    statistic, p_value = kruskal(*groups)
    
    # Perform pairwise Mann-Whitney U tests with Bonferroni correction
    if p_value < alpha:
        # Extract group names
        group_names = data_filtered['Treatment'].unique()
        
        # Perform pairwise comparisons
        significant_comparisons = []
        for i in range(len(group_names)):
            for j in range(i+1, len(group_names)):
                u_statistic, u_p_value = mannwhitneyu(groups[i], groups[j], alternative='two-sided')
                adjusted_alpha = alpha / (len(group_names) * (len(group_names) - 1) / 2)  # Bonferroni correction
                if u_p_value < adjusted_alpha:
                    significant_comparisons.append((group_names[i], group_names[j], u_p_value))  # Include p-value in the tuple
        
        # Append results
        results.append({'Column': column, 'Test Statistic': statistic, 'P-value': p_value, 'Significance': 'Significant',
                        'Significant Comparisons': significant_comparisons})
    else:
        results.append({'Column': column, 'Test Statistic': statistic, 'P-value': p_value, 'Significance': 'Not Significant'})

# Create a DataFrame from the results
results_df = pd.DataFrame(results)

# Write the results to an Excel file
output_file = 'Kruskal_Wallis_Results_with_Comparisons.xlsx'
results_df.to_excel(output_file, index=False)

print(f"Results saved to '{output_file}'")
