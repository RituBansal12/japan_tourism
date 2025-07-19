import pandas as pd
import matplotlib.pyplot as plt
import os
from plot_config import *

# Read the CSV file
csv_path = os.path.join('raw_data', 'travel_costs.csv')
df = pd.read_csv(csv_path)

# Remove $ from spend columns and convert to float
df['CPI_adjusted_daily_spend'] = df['CPI_adjusted_daily_spend'].replace({'\$': ''}, regex=True).astype(float)
df['Year'] = df['Year'].astype(int)

# Set up the plot
plt.figure(figsize=(12, 7))

# Plot each country
for country in df['Country'].unique():
    country_data = df[df['Country'] == country]
    plt.plot(
        country_data['Year'],
        country_data['CPI_adjusted_daily_spend'],
        marker='o',
        label=country
    )

plt.xlabel('Year', **STANDARD_LABEL_CONFIG)
plt.ylabel('Inflation Adjusted Daily Spend (USD)', **STANDARD_LABEL_CONFIG)
plt.title('Inflation Adjusted Daily Spend by Country (2010-2024)', **STANDARD_TITLE_CONFIG)
plt.legend(title='Country')
plt.grid(True, **STANDARD_GRID_CONFIG)
plt.tight_layout()
plt.savefig('visualizations/travel_costs_cpi_adjusted.png', **STANDARD_FIGURE_CONFIG)
plt.close()

# --- Yearly Total Spend by Tourists (Yen & USD) ---
import numpy as np

# Read per capita spend (Yen)
spend_df = pd.read_csv(os.path.join('raw_data', 'spend_per_capita.csv'))
spend_df.columns = [c.strip() for c in spend_df.columns]
spend_df['Year'] = spend_df['Year'].astype(int)
spend_df['Consumption Amount'] = spend_df['Consumption Amount'].replace({',': ''}, regex=True).astype(int)

# Read and aggregate yearly tourist numbers
visitors_df = pd.read_csv(os.path.join('raw_data', 'cleaned_visitors.csv'))
visitors_df['year'] = visitors_df['year'].astype(int)
# Only use rows with valid tourist numbers
visitors_df = visitors_df[pd.notnull(visitors_df['tourist'])]
visitors_df['tourist'] = visitors_df['tourist'].astype(int)
yearly_tourists = visitors_df.groupby('year')['tourist'].sum().reset_index()

# Merge with spend data (2011-2024 intersection)
years = list(range(2011, 2025))
spend_df = spend_df[spend_df['Year'].isin(years)]
yearly_tourists = yearly_tourists[yearly_tourists['year'].isin(years)]
merged = pd.merge(spend_df, yearly_tourists, left_on='Year', right_on='year', how='inner')

# JPY to USD average yearly rates (from internet, exchange-rates.org, 2011-2024)
jpy_usd_rates = {
    2011: 0.0125, 2012: 0.0126, 2013: 0.0105, 2014: 0.0095, 2015: 0.0083,
    2016: 0.0092, 2017: 0.0089, 2018: 0.0091, 2019: 0.0092, 2020: 0.0093,
    2021: 0.0091, 2022: 0.0077, 2023: 0.0073, 2024: 0.0066
}

# Calculate total spend in Yen and USD
total_spend_yen = merged['Consumption Amount'] * merged['tourist']
merged['Total Spend (Yen)'] = total_spend_yen
merged['JPYtoUSD'] = merged['Year'].map(jpy_usd_rates)
merged['Total Spend (USD)'] = merged['Total Spend (Yen)'] * merged['JPYtoUSD']

# Remove years with unreliable data
remove_years = [2020, 2021, 2022]
plot_years = [y for y in years if y not in remove_years]
merged_plot = merged[merged['Year'].isin(plot_years)]

# Plot vertical bar chart (YoY, 2011-2024, excluding 2020, 2021, 2022)
plt.figure(figsize=(12, 7))
year_labels = [str(y) for y in merged_plot['Year']]
bar = plt.bar(year_labels, merged_plot['Total Spend (USD)'] / 1e9, color=COLOR_PALETTE[0])
plt.xlabel('Year', **STANDARD_LABEL_CONFIG)
plt.ylabel('Total Spend by Tourists (Billion USD)', **STANDARD_LABEL_CONFIG)
plt.title('Total Yearly Spend by Tourists in Japan (2011-2024 Excl. Covid Era)', **STANDARD_TITLE_CONFIG)
plt.grid(True, **STANDARD_GRID_CONFIG)
plt.tight_layout()

# Show only present years on the x-axis (no gaps for removed years)
plt.xticks(year_labels, year_labels)

# Add value labels on top of bars (e.g., $5B)
for rect in bar:
    height = rect.get_height()
    label = f"${height:.1f}B"
    plt.text(rect.get_x() + rect.get_width() / 2, height, label, ha='center', va='bottom', fontsize=12)

plt.savefig('visualizations/total_yearly_spend_usd.png', **STANDARD_FIGURE_CONFIG)
plt.close() 