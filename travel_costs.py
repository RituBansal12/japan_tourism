import pandas as pd
import matplotlib.pyplot as plt
import os

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

plt.xlabel('Year')
plt.ylabel('InflationAdjusted Daily Spend (USD)')
plt.title('Inflation Adjusted Daily Spend by Country (2010-2024)')
plt.legend(title='Country')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('visualizations/travel_costs_cpi_adjusted.png')
plt.show() 