import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import font_manager
import warnings
warnings.filterwarnings('ignore')
import bar_chart_race as bcr
from plot_config import *

# Create visualizations folder if it doesn't exist
import os
if not os.path.exists('visualizations'):
    os.makedirs('visualizations')

# Load the cleaned data
df = pd.read_csv('raw_data/cleaned_visitors.csv')

# Convert year to datetime for better plotting
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'] + '-01')

# Filter out "Unclassified" countries and 2025 data
df = df[~df['country'].str.contains('Unclassified', na=False)]
df = df[df['year'] <= 2024]



# 1. Total Tourists Over Time
def plot_total_visitors_growth():
    # Aggregate by year using tourist data
    yearly_data = df.groupby('year')['tourist'].sum().reset_index()
    yearly_data = yearly_data.sort_values('year')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Plot total tourists (in millions) with darker color
    line = ax.plot(yearly_data['year'], yearly_data['tourist'] / 1e6, 
                   color='#1f1f1f', linewidth=4, marker='o', markersize=8)
    
    ax.set_xlabel('Year', **STANDARD_LABEL_CONFIG)
    ax.set_ylabel('Total Tourists (In Millions)', **STANDARD_LABEL_CONFIG)
    ax.set_title('Japan Tourism: Total Tourists (1996-2024)', **STANDARD_TITLE_CONFIG)
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels 90 degrees
    ax.tick_params(axis='x', rotation=90)
    
    # Set all years on x-axis
    all_years = sorted(df['year'].unique())
    ax.set_xticks(all_years)
    ax.set_xticklabels(all_years, rotation=90)
    
    # Add COVID period markers
    covid_start = 2020
    covid_end = 2022
    ax.axvspan(covid_start, covid_end, alpha=0.3, color='red', label='COVID Period')
    ax.axvline(x=covid_start, color='red', linestyle='--', alpha=0.7, linewidth=2)
    ax.axvline(x=covid_end, color='red', linestyle='--', alpha=0.7, linewidth=2)
    
    # Add legend
    ax.legend(loc='upper left')
    
    plt.tight_layout()
    plt.savefig('visualizations/total_visitors_growth.png', **STANDARD_FIGURE_CONFIG)
    plt.close()

# 3. Top 10 Countries by Tourist Count (2023-2024) - Sorted in descending order
def plot_top_countries():
    # Calculate total tourists by country for 2023-2024
    recent_data = df[df['year'].isin([2023, 2024])]
    country_totals = recent_data.groupby('country')['tourist'].sum().reset_index()
    top_10_countries = country_totals.nlargest(10, 'tourist').sort_values('tourist', ascending=True)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Use seaborn flare color palette
    colors = COLOR_PALETTE[:len(top_10_countries)]
    bars = ax.barh(top_10_countries['country'], top_10_countries['tourist'] / 1e6, 
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    
    ax.set_title('Top 10 Countries by Tourist Visitors to Japan (2023-2024)', **STANDARD_TITLE_CONFIG)
    ax.set_xlabel('Total Tourists (In Millions)', **STANDARD_LABEL_CONFIG)
    ax.set_ylabel('Country', **STANDARD_LABEL_CONFIG)
    
    # Add value labels on bars
    for bar, total in zip(bars, top_10_countries['tourist']):
        width = bar.get_width()
        ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2,
               f'{total/1e6:.1f}M', ha='left', va='center', fontweight='bold')
    
    # Format x-axis with millions
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1f}M'))
    
    plt.tight_layout()
    plt.savefig('visualizations/top_10_countries.png', **STANDARD_FIGURE_CONFIG)
    plt.close()

# 4. Top 10 Countries with Highest Post-COVID Growth - Sorted in descending order
def plot_post_covid_growth():
    # Calculate 2011 and 2024 totals by country
    pre_period = df[df['year'] == 2011].groupby('country')['tourist'].sum().reset_index()
    post_period = df[df['year'] == 2024].groupby('country')['tourist'].sum().reset_index()
    
    # Merge and calculate growth
    growth_data = pre_period.merge(post_period, on='country', suffixes=('_2011', '_2024'))
    growth_data['growth_percentage'] = ((growth_data['tourist_2024'] - growth_data['tourist_2011']) / 
                                       growth_data['tourist_2011']) * 100
    
    # Get top 10 by growth percentage and sort in descending order
    top_10_growth = growth_data.nlargest(10, 'growth_percentage').sort_values('growth_percentage', ascending=True)
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Use the mixed palette for consistency
    colors = COLOR_PALETTE[:len(top_10_growth)]
    bars = ax.barh(top_10_growth['country'], top_10_growth['growth_percentage'], 
                   color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    
    ax.set_title('Top 10 Countries with Highest Growth (2011 vs 2024)', **STANDARD_TITLE_CONFIG)
    ax.set_xlabel('Growth Percentage (%)', **STANDARD_LABEL_CONFIG)
    ax.set_ylabel('Country', **STANDARD_LABEL_CONFIG)
    
    # Add percentage labels on bars (rounded, no decimals)
    for bar, pct in zip(bars, top_10_growth['growth_percentage']):
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2,
               f'{int(round(pct))}%', ha='left', va='center', fontweight='bold')
    
    # Add a vertical line at 0%
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('visualizations/top_10_highest_growth.png', **STANDARD_FIGURE_CONFIG)
    plt.close()

def plot_monthly_distribution_heatmap():
    # Prepare data: map full month names to abbreviations
    month_full_to_abbr = {
        'January': 'Jan', 'February': 'Feb', 'March': 'Mar', 'April': 'Apr',
        'May': 'May', 'June': 'Jun', 'July': 'Jul', 'August': 'Aug',
        'September': 'Sep', 'October': 'Oct', 'November': 'Nov', 'December': 'Dec',
        'Jan': 'Jan', 'Feb': 'Feb', 'Mar': 'Mar', 'Apr': 'Apr',
        'Jun': 'Jun', 'Jul': 'Jul', 'Aug': 'Aug', 'Sep': 'Sep', 'Oct': 'Oct', 'Nov': 'Nov', 'Dec': 'Dec'
    }
    df['month'] = df['month'].map(month_full_to_abbr).fillna(df['month'])

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df['month'] = pd.Categorical(df['month'], categories=month_order, ordered=True)
    
    # Exclude 2020, 2021, 2022
    filtered_df = df[~df['year'].isin([2020, 2021, 2022])]
    
    # Group by year and month, sum tourists
    monthly = filtered_df.groupby(['year', 'month'])['tourist'].sum().reset_index()
    
    # Calculate total tourists per year
    yearly_totals = monthly.groupby('year')['tourist'].sum().reset_index().rename(columns={'tourist': 'year_total'})
    monthly = monthly.merge(yearly_totals, on='year')
    # Calculate percentage
    monthly['pct_of_year'] = (monthly['tourist'] / monthly['year_total']) * 100
    
    # Pivot for heatmap
    heatmap_data = monthly.pivot(index='year', columns='month', values='pct_of_year').reindex(columns=month_order)
    
    # Create heatmap with single color (blue) and no annotations
    plt.figure(figsize=(14, 12))
    sns.heatmap(
        heatmap_data,
        cmap=sns.light_palette('#2066a8', as_cmap=True),
        linewidths=0.5,
        linecolor='white',
        annot=False,
        cbar_kws={'label': '% of Annual Tourists'}
    )
    plt.title('Monthly Distribution of Tourists as % of Annual Total', **STANDARD_TITLE_CONFIG)
    plt.xlabel('Month', **STANDARD_LABEL_CONFIG)
    plt.ylabel('Year', **STANDARD_LABEL_CONFIG)
    plt.xticks(fontsize=12, fontweight='normal')
    plt.yticks(fontsize=12, fontweight='normal')
    plt.tight_layout()
    plt.savefig('visualizations/monthly_distribution_heatmap.png', **STANDARD_FIGURE_CONFIG)
    plt.close()


def animate_top_15_countries():
    # Only include years 2001-2019 and 2023-2024 (exclude 2020-2022)
    valid_years = list(range(2001, 2020)) + [2023, 2024]
    sub_df = df[df['year'].isin(valid_years)]
    # Prepare data: sum by year and country
    yearly_country = sub_df.groupby(['year', 'country'])['tourist'].sum().reset_index()
    # Pivot for bar_chart_race: index=year, columns=country, values=tourist
    pivot = yearly_country.pivot(index='year', columns='country', values='tourist').fillna(0)
    # MP4 export (high quality)
    bcr.bar_chart_race(
        df=pivot,
        filename='visualizations/top_15_countries_barchart_race.mp4',
        orientation='h',
        sort='desc',
        n_bars=15,
        period_length=2500,  # 2.5 seconds per year, total duration < 1 min
        interpolate_period=True,
        title='Top 15 Countries by Tourism Visitors to Japan (2001-2024)\nExcluding Covid Era (2020-2022)',
        title_size=20,  # Bold title size
        bar_size=.95,
        period_label=True,
        period_fmt='{x:.0f}',  # Show year as integer without decimal
        cmap=['#2066a8'],  # Use custom blue color for all bars
        filter_column_colors=False,  # Disable to use single color
        figsize=(16, 9),
        dpi=144,
        writer='ffmpeg',
        steps_per_period=30,  # More frames for smoother animation
        tick_label_size=12,  # Larger y-axis labels
        shared_fontdict={'weight': 'bold'}  # Make all text bold
    )
    # GIF export (smaller size, smoother)
    bcr.bar_chart_race(
        df=pivot,
        filename='visualizations/top_15_countries_barchart_race.gif',
        orientation='h',
        sort='desc',
        n_bars=15,
        period_length=2500,  # 2.5 seconds per year
        interpolate_period=True,
        title='Top 15 Countries by Tourism Visitors to Japan (2001-2024)\nExcluding Covid Era (2020-2022)',
        title_size=16,  # Slightly smaller title for GIF
        bar_size=.95,
        period_label=True,
        period_fmt='{x:.0f}',
        cmap=['#2066a8'],
        filter_column_colors=False,
        figsize=(9, 5.5),  # More compact for GIF
        dpi=100,           # Lower DPI for smaller file
        writer='imagemagick',
        steps_per_period=20,  # Smoother animation
        tick_label_size=10,
        shared_fontdict={'weight': 'bold'}
    )

def plot_two_period_growth_comparison():
    # Load global data
    global_data = pd.read_csv('raw_data/tourism_top_10_countries.csv')
    global_data['Total_tourists'] = global_data['Total_tourists'].str.replace(',', '').astype(float)
    
    # Get the list of top 10 countries (excluding Japan)
    top_countries = global_data['Country'].unique().tolist()
    if 'Japan' in top_countries:
        top_countries.remove('Japan')
    
    # Aggregate Japan's total tourism for 2014, 2019, 2024
    japan_years = [2014, 2019, 2024]
    japan_agg = (
        df[df['year'].isin(japan_years)]
          .groupby('year')['tourist'].sum()
          .reset_index()
          .rename(columns={'year': 'Year', 'tourist': 'Total_tourists'})
    )
    japan_agg['Country'] = 'Japan'
    
    # Build a combined dataframe for all countries (10 + Japan)
    all_countries = top_countries + ['Japan']
    records = []
    for country in all_countries:
        if country == 'Japan':
            for y in japan_years:
                val = japan_agg[japan_agg['Year'] == y]['Total_tourists']
                if not val.empty:
                    records.append({'Country': 'Japan', 'Year': y, 'Total_tourists': val.values[0]})
        else:
            for y in japan_years:
                val = global_data[(global_data['Country'] == country) & (global_data['Year'] == y)]['Total_tourists']
                if not val.empty:
                    records.append({'Country': country, 'Year': y, 'Total_tourists': val.values[0]})
    combined = pd.DataFrame(records)
    
    # Calculate growth rates for each country
    growth_data = []
    for country in all_countries:
        cdata = combined[combined['Country'] == country]
        y2014 = cdata[cdata['Year'] == 2014]['Total_tourists']
        y2019 = cdata[cdata['Year'] == 2019]['Total_tourists']
        y2024 = cdata[cdata['Year'] == 2024]['Total_tourists']
        if not (y2014.empty or y2019.empty or y2024.empty):
            growth_14_19 = ((y2019.values[0] - y2014.values[0]) / y2014.values[0]) * 100
            growth_19_24 = ((y2024.values[0] - y2019.values[0]) / y2019.values[0]) * 100
            growth_data.append({
                'Country': country,
                'Growth_2014_2019': growth_14_19,
                'Growth_2019_2024': growth_19_24
            })
    growth_df = pd.DataFrame(growth_data)
    # Sort to put Japan first, then by 2019-2024 growth for visual clarity
    growth_df['is_japan'] = growth_df['Country'] == 'Japan'
    growth_df = growth_df.sort_values(['is_japan', 'Growth_2019_2024'], ascending=[False, False])
    growth_df = growth_df.drop('is_japan', axis=1)
    
    # Plot grouped bar chart
    x = np.arange(len(growth_df))
    width = 0.35
    fig, ax = plt.subplots(figsize=(20, 10))  # Increased width to accommodate all 11 countries
    
    # Use consistent colors for all countries
    period1_color = '#2066a8'  # Dark blue for 2014→2019
    period2_color = '#ae282c'  # Dark red for 2019→2024
    
    bars1 = ax.bar(x - width/2, growth_df['Growth_2014_2019'], width, label='2014→2019', color=period1_color, alpha=0.8)
    bars2 = ax.bar(x + width/2, growth_df['Growth_2019_2024'], width, label='2019→2024', color=period2_color, alpha=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(growth_df['Country'], rotation=0, ha='center', fontsize=11)  # No rotation, smaller font
    ax.set_ylabel('Growth Rate (%)', **STANDARD_LABEL_CONFIG)
    ax.set_title('Top Global Destinations: Tourism Growth Rate', **STANDARD_TITLE_CONFIG)
    ax.legend(fontsize=12)
    ax.grid(True, axis='y', alpha=0.3)
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1, f'{height:.1f}%', ha='center', va='bottom', fontsize=10)
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1, f'{height:.1f}%', ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    plt.savefig('visualizations/two_period_growth_comparison.png', **STANDARD_FIGURE_CONFIG)
    plt.close()

def plot_stacked_region_distribution():
    df2 = df.copy()
    # Exclude unreliable years (2020-2022) and Africa
    df2 = df2[~df2['year'].isin([2020, 2021, 2022])]
    df2 = df2[df2['region'] != 'Africa']
    # Aggregate total tourists per year and region
    agg = df2.groupby(['year', 'region'])['tourist'].sum().reset_index()
    # Pivot to get regions as columns
    pivot = agg.pivot_table(index='year', columns='region', values='tourist', fill_value=0)
    # Calculate percentages
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100
    # Convert years to string to avoid gaps and reverse order for plotting
    year_labels = [str(y) for y in pivot_pct.index]
    year_labels = year_labels[::-1]  # Reverse so most recent is at the bottom
    pivot_pct = pivot_pct.iloc[::-1]  # Reverse DataFrame rows to match
    # Use distinct, contrasting colors for regions
    region_list = list(pivot_pct.columns)
    palette_len = len(COLOR_PALETTE)
    color_indices = list(range(0, palette_len, max(1, palette_len // len(region_list))))
    colors = [COLOR_PALETTE[i % palette_len] for i in color_indices[:len(region_list)]]
    # Plot horizontal stacked bar chart
    plt.figure(figsize=(16, 10))
    bottom = None
    for i, region in enumerate(region_list):
        plt.barh(year_labels, pivot_pct[region], left=bottom, label=region, color=colors[i])
        if bottom is None:
            bottom = pivot_pct[region].copy()
        else:
            bottom += pivot_pct[region]
    plt.xlabel('Percentage of Total Tourists (%)', **STANDARD_LABEL_CONFIG)
    plt.ylabel('Year', **STANDARD_LABEL_CONFIG)
    plt.title('Tourist Region Distribution by Year (Excl. Covid Era)', **STANDARD_TITLE_CONFIG)
    plt.xlim(0, 100)
    plt.grid(True, axis='x', **STANDARD_GRID_CONFIG)
    # Place legend in a single line at the bottom
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=len(region_list), frameon=False)
    plt.tight_layout(rect=[0, 0.08, 1, 1])
    plt.savefig('visualizations/stacked_region_distribution.png', **STANDARD_FIGURE_CONFIG)
    plt.close()

# Main execution
if __name__ == "__main__":
    print("Creating visualizations...")
    
    # Create all visualizations
    plot_total_visitors_growth()
    print("Total visitors growth chart created")
        
    plot_top_countries()
    print("Top 10 countries chart created")
    
    plot_post_covid_growth()
    print("Post-COVID growth chart created")
    
    plot_monthly_distribution_heatmap()
    print("Monthly distribution heatmap created")
    
    animate_top_15_countries()
    print("Top 15 countries bar chart race animation created")
    
    plot_two_period_growth_comparison()
    print("Two-period growth comparison chart created")
    
    plot_stacked_region_distribution()
    print("Stacked bar chart (region distribution) created")
    
    print("\nAll visualizations saved in the 'visualizations' folder!") 