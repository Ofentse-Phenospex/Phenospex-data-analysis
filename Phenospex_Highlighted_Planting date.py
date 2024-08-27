# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 10:58:03 2024

@author: u14093767
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read data from Excel sheet
data = pd.read_excel('C:/Users/u14093767/Desktop/Phenospex raw data/Maize_Combined_Day_Number.xlsx')

# Clip the number of days elapsed so that it stops at day 70 for November
data.loc[data['Treatment'] == 'November 2021', 'Day after planting'] = data[data['Treatment'] == 'November 2021']['Day after planting'].clip(upper=70)

# Clip the number of days elapsed so that it stops at day 80 for other treatments
data.loc[data['Treatment'] != 'November 2021', 'Day after planting'] = data[data['Treatment'] != 'November 2021']['Day after planting'].clip(upper=80)

# Replace 'categorical_column' and 'data_columns' with actual column names
categorical_column = 'Treatment'
data_columns = ['Digital biomass [mm³]', 'Greenness average', 'Height [mm]', 'Leaf area [mm²]',
                'Leaf area index [mm²/mm²]', 'Leaf area (projected) [mm²]', 'Leaf inclination [mm²/mm²]',
                'Light penetration depth [mm]', 'NDVI average', 'NPCI average', 'PSRI average', 'Height Max [mm]', 'Leaf angle [°]']

# Create a folder to save the figures if it doesn't exist
output_folder = os.path.join(os.path.expanduser("~"), "Desktop", "leaf_angle_distribution_line_graphs")
os.makedirs(output_folder, exist_ok=True)

# Determine the maximum day after planting across all treatments
max_day_after_planting = data['Day after planting'].max()

for col in data_columns:
    plt.figure(figsize=(12, 8))
    
    # Iterate over treatments
    treatments = data[categorical_column].unique()
    for i, treatment in enumerate(treatments):
        treatment_data = data[data[categorical_column] == treatment]
        x = treatment_data['Day after planting']
        y = treatment_data[col]
        
        # Fit polynomial regression line
        z = np.polyfit(x, y, 3)
        p = np.poly1d(z)
        
        # Generate points for smooth curve
        x_smooth = np.linspace(x.min(), x.max(), 100)
        y_smooth = p(x_smooth)
        
        # Calculate residuals
        residuals = y - p(x)
        mean_residual = np.mean(residuals)
        std_residual = np.std(residuals)
        
        # Define bounds for highlights closely following trendlines
        upper_bound = y_smooth + 2 * std_residual
        lower_bound = y_smooth - 2 * std_residual
        
        # Plot trendline
        plt.plot(x_smooth, y_smooth, label=f'({treatment})', linestyle='-', color=f'C{i}')
        
        # Fill between the bounds
        plt.fill_between(x_smooth, lower_bound, upper_bound, color=f'C{i}', alpha=0.2, label='_nolegend_')  # Adjust the spread as needed
    
    plt.xlabel('Days after planting', fontsize=20)
    plt.ylabel(col, fontsize=20)
    plt.xticks(fontsize=20, rotation=45, color='black')  # Set x-axis tick color to black
    plt.yticks(fontsize=20, color='black')  # Set y-axis tick color to black
    plt.xlim(0, max_day_after_planting)  # Set x-axis limit based on the maximum day after planting
    
    # Set white background
    plt.gca().set_facecolor('white')
    
    # Set x and y axis color to black
    plt.gca().spines['bottom'].set_color('black')
    plt.gca().spines['left'].set_color('black')
    
    # Ensure major ticks are visible on the y-axis
    plt.gca().tick_params(axis='y', direction='out', colors='black', width=2, length=10)
    
    # Set major tick marks on y-axis
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(nbins=5))
    
    # Create a separate legend outside the graph
    legend = plt.legend(loc='upper left', title=categorical_column, fontsize=20, bbox_to_anchor=(1.05, 1))
    plt.setp(legend.get_title(), fontsize=20)
    
    plt.tight_layout()

    # Save the figure to the output folder
    output_path = os.path.join(output_folder, f'{col.replace("/", "_").replace("[", "_").replace("]", "_")}_highlighted_distribution_line_graph.png')
    plt.savefig(output_path, bbox_inches='tight', facecolor='white')  # Save with tight layout and white background

    plt.close()  # Close the figure to free up resources

# Optional: Show a message indicating where the figures were saved
print("Graphs saved in the folder:", output_folder)
