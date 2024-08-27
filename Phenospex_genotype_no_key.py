# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 10:58:01 2024

@author: u14093767
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read data from Excel sheet
data = pd.read_excel('C:/Users/u14093767/Desktop/Phenospex raw data/Maize_Combined_Day_Number.xlsx')

# Clip the number of days elapsed so that it stops at day 60 and starts at day 30 for all treatments
data['Day after planting'] = data['Day after planting'].clip(lower=30, upper=60)

# Clip height at 900 mm
data['Height [mm]'] = data['Height [mm]'].clip(upper=900)

# Replace 'categorical_column' and 'data_columns' with actual column names
categorical_column = 'Genotype'
data_columns = ['Digital biomass [mm³]', 'Greenness average', 'Height [mm]', 'Leaf area [mm²]',
                'Leaf area index [mm²/mm²]', 'Leaf area (projected) [mm²]', 'Leaf inclination [mm²/mm²]',
                'Light penetration depth [mm]', 'NDVI average', 'NPCI average', 'PSRI average', 'Height Max [mm]']

# Create a folder to save the figures if it doesn't exist
output_folder = os.path.join(os.path.expanduser("~"), "Desktop", "highlighted_distribution_line_graphs_genotype")
os.makedirs(output_folder, exist_ok=True)

# Assign a color to each genotype
genotypes = data[categorical_column].unique()
colors = {genotype: f'C{i}' for i, genotype in enumerate(genotypes)}

for treatment in data['Treatment'].unique():
    for col in data_columns:
        plt.figure(figsize=(12, 8))
        
        # Filter data for the current treatment
        treatment_data = data[data['Treatment'] == treatment]
        
        # Iterate over genotypes within the treatment
        for genotype in genotypes:
            genotype_data = treatment_data[treatment_data[categorical_column] == genotype]
            x = genotype_data['Day after planting']
            y = genotype_data[col]
            
            # Fit polynomial regression line
            z = np.polyfit(x, y, 3)
            p = np.poly1d(z)
            
            # Generate points for smooth curve
            x_smooth = np.linspace(x.min(), x.max(), 100)
            y_smooth = p(x_smooth)
            
            # Calculate standard error
            residuals = y - p(x)
            standard_error = np.std(residuals) / np.sqrt(len(residuals))
            
            # Define bounds for highlights using standard error
            upper_bound = y_smooth + 2 * standard_error
            lower_bound = y_smooth - 2 * standard_error
            
            # Plot trendline
            plt.plot(x_smooth, y_smooth, linestyle='-', color=colors[genotype])
            
            # Fill between the bounds
            plt.fill_between(x_smooth, lower_bound, upper_bound, color=colors[genotype], alpha=0.2, label='_nolegend_')
    
        plt.xlabel('Days after planting', fontsize=20)
        plt.ylabel(col, fontsize=20)
        plt.xticks(fontsize=20, rotation=45, color='black')  # Set x-axis tick color to black
        plt.yticks(fontsize=20, color='black')  # Set y-axis tick color to black
        plt.xlim(30, 60)  # Set x-axis limit from 30 to 60 days after planting
        
        # Set white background
        plt.gca().set_facecolor('white')
        
        # Show only x and y axis
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['bottom'].set_color('black')
        plt.gca().spines['left'].set_color('black')
        
        # Ensure major ticks are visible on the y-axis
        plt.gca().tick_params(axis='y', direction='out', colors='black', width=2, length=10)
        
        # Set major tick marks on y-axis
        plt.gca().yaxis.set_major_locator(plt.MaxNLocator(nbins=5))
        
        plt.tight_layout()

        # Save the figure to the output folder
        output_path = os.path.join(output_folder, f'{col.replace("/", "_").replace("[", "_").replace("]", "_")}_highlighted_distribution_line_graph_{treatment}.png')
        plt.savefig(output_path, bbox_inches='tight', facecolor='white')  # Save with tight layout and white background

        plt.close()  # Close the figure to free up resources

# Optional: Show a message indicating where the figures were saved
print("Graphs saved in the folder:", output_folder)




