# -*- coding: utf-8 -*-
"""
Created on Fri May  3 09:52:00 2024

@author: u14093767
"""

import os
import pandas as pd
import seaborn as sns
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

# Read data from Excel sheet
data = pd.read_excel('C:/Users/u14093767/Desktop/Phenospex raw data/Maize_Combined_Day_Number.xlsx')

# Filter data to start at day 30 and end at day 80
data_filtered = data[(data['Day after planting'] >= 35) & (data['Day after planting'] <= 60)]

# Remove columns where height exceeds 1000 mm
data_filtered = data_filtered[data_filtered['Height [mm]'] <= 999]

# Define the columns of interest
columns_of_interest = ['Digital biomass [mm³]', 'Height [mm]', 'Leaf area index ',
                       'Light penetration depth [mm]', 'NDVI average', 'Greenness average',
                       'NPCI average', 'PSRI average']

# Create a folder to save the heatmaps if it doesn't exist
output_folder = os.path.join(os.path.expanduser("~"), "Desktop", "pairwise_mannwhitneyu_heatmaps")
os.makedirs(output_folder, exist_ok=True)

# Mapping months to the desired abbreviated format
month_mapping = {
    'December 2021,': 'Dec',
    'November 2021,': 'Nov',
    'January 2022,': 'Jan',
    'February 2022,': 'Feb'
}

# Create a heatmap for each column
for column in columns_of_interest:
    # Create an empty DataFrame to store the p-values
    p_values_df = pd.DataFrame(index=data_filtered['Treatment'].unique(), columns=data_filtered['Treatment'].unique())

    # Perform pairwise Mann-Whitney U tests for each pair of treatments
    treatments = data_filtered['Treatment'].unique()
    for i, treatment_i in enumerate(treatments):
        for j, treatment_j in enumerate(treatments):
            if i < j:  # Only perform tests for unique pairs
                data_i = data_filtered[data_filtered['Treatment'] == treatment_i][column]
                data_j = data_filtered[data_filtered['Treatment'] == treatment_j][column]
                statistic, p_value = mannwhitneyu(data_i, data_j, alternative='two-sided')
                # Store the p-value in the DataFrame
                p_values_df.loc[treatment_j, treatment_i] = p_value

    # Convert p-values to numeric values and filter significant values
    p_values_df = p_values_df.astype(float)
    significance_mask = p_values_df < 0.05
    p_values_df[significance_mask] = 1
    p_values_df[~significance_mask] = 0

    # Create a heatmap
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(p_values_df, cmap=ListedColormap(['white', 'grey']), annot=False, cbar=False, linewidths=1)

    # Align the x and y labels to the center of each cell
    ax.set_xticks(np.arange(p_values_df.shape[1]) + 0.5, minor=False)
    ax.set_yticks(np.arange(p_values_df.shape[0]) + 0.5, minor=False)
    ax.set_xticklabels([month_mapping.get(label, label) for label in p_values_df.columns], fontsize=50, rotation=45)
    ax.set_yticklabels([month_mapping.get(label, label) for label in p_values_df.index], fontsize=50, rotation=0)

    ax.set_title('')
    plt.xlabel('')
    plt.ylabel('')
    
    plt.tight_layout()

    # Save the heatmap to the output folder
    output_path = os.path.join(output_folder, f'{column}_pairwise_mannwhitneyu_heatmap.png')
    plt.savefig(output_path)
    plt.close()

print("Heatmaps saved in the folder:", output_folder)






