import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import font_manager
import warnings
warnings.filterwarnings('ignore')
import bar_chart_race as bcr

# Set up sophisticated fonts
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Georgia']
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['figure.titlesize'] = 20

# Create visualizations folder if it doesn't exist
import os
if not os.path.exists('visualizations'):
    os.makedirs('visualizations')

# Load the cleaned data
df = pd.read_csv('processed_data/cleaned_visitors.csv')

# Convert year to datetime for better plotting
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'] + '-01')

# Filter out "Unclassified" countries and 2025 data
df = df[~df['country'].str.contains('Unclassified', na=False)]
df = df[df['year'] <= 2024]

# Use custom divergent color palette (expanded to 10 colors)
COLOR_PALETTE = [
    '#2066a8',  # Dark Blue
    '#3a7fc2',  # Between Dark & Med Blue
    '#8ec1da',  # Med Blue
    '#a7d3e4',  # Between Med & Light Blue
    '#cde1ec',  # Light Blue (fixed typo)
    '#ededed',  # Gray
    '#f6d6c2',  # Light Red
    '#efb09a',  # Between Light & Med Red
    '#d47264',  # Med Red
    '#ae282c'   # Dark Red
]

# 1. Total Tourists Over Time (Simplified)
def plot_total_visitors_growth():
    # Aggregate by year using tourist data
    yearly_data = df.groupby('year')['tourist'].sum().reset_index()
    yearly_data = yearly_data.sort_values('year')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Plot total tourists (in millions) with darker color
    line = ax.plot(yearly_data['year'], yearly_data['tourist'] / 1e6, 
                   color='#1f1f1f', linewidth=4, marker='o', markersize=8)
    
    ax.set_xlabel('Year', fontweight='bold')
    ax.set_ylabel('Total Tourists (In Millions)', fontweight='bold')
    ax.set_title('Japan Tourism: Total Tourists (1996-2024)', 
                fontweight='bold', pad=20)
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
    plt.savefig('visualizations/total_visitors_growth.png', dpi=300, bbox_inches='tight')
    plt.close()

# 2. Regional Distribution Stacked Bar Chart (1996-2024, 5-year intervals)
def plot_regional_maps():
    # Define non-overlapping intervals
    intervals = [
        (1996, 2000),
        (2001, 2005),
        (2006, 2010),
        (2011, 2015),
        (2016, 2020),
        (2021, 2024)
    ]
    interval_labels = [f"{start}-{end}" for start, end in intervals]
    
    # Assign each row to an interval
    def assign_interval(year):
        for i, (start, end) in enumerate(intervals):
            if start <= year <= end:
                return interval_labels[i]
        return None
    
    df['period'] = df['year'].apply(assign_interval)
    regional_data = df[df['period'].notnull()]
    
    # Remove Africa from the data
    regional_data = regional_data[regional_data['region'] != 'Africa']
    
    # Aggregate by period and region
    regional_by_period = regional_data.groupby(['period', 'region'])['tourist'].sum().reset_index()
    regional_pivot = regional_by_period.pivot(index='period', columns='region', values='tourist').fillna(0)
    
    # Calculate percentages for 100% stacked bar chart
    regional_pivot_percent = regional_pivot.div(regional_pivot.sum(axis=1), axis=0) * 100
    
    # Use a mix of distinct red, blue, and grey shades from the palette
    mixed_palette = ['#2066a8', '#8ec1da', '#ededed', '#f6d6c2', '#ae282c']
    n_regions = len(regional_pivot_percent.columns)
    colors = mixed_palette[:n_regions]
    
    # Create stacked bar chart
    fig, ax = plt.subplots(figsize=(14, 8))
    regional_pivot_percent.plot(kind='bar', stacked=True, ax=ax, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    
    ax.set_title('Breakdown of Tourists by Region', fontweight='bold', pad=20)
    ax.set_ylabel('Percentage of Tourists (%)', fontweight='bold')
    ax.set_xlabel('Period', fontweight='bold')
    
    # Set x-axis labels (horizontal, smaller font)
    ax.set_xticklabels(interval_labels, fontsize=10, rotation=0)
    
    # Place legend at the bottom in a single horizontal line, with less space below x-axis
    legend = ax.legend(title='Region', bbox_to_anchor=(0.5, -0.10), loc='upper center', ncol=n_regions, frameon=False)
    
    # Add note just below the legend, but above the bottom edge
    plt.figtext(0.5, 0.025, 'Note: Africa is excluded due to negligible percentage.', ha='center', fontsize=11, color='gray')
    
    # Format y-axis as percentages
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0f}%'))
    ax.set_ylim(0, 100)
    
    plt.tight_layout(rect=[0, 0.08, 1, 1])
    plt.savefig('visualizations/regional_distribution_maps.png', dpi=300, bbox_inches='tight')
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
    
    ax.set_title('Top 10 Countries by Tourist Visitors to Japan (2023-2024)', 
                fontweight='bold', pad=20)
    ax.set_xlabel('Total Tourists (In Millions)', fontweight='bold')
    ax.set_ylabel('Country', fontweight='bold')
    
    # Add value labels on bars
    for bar, total in zip(bars, top_10_countries['tourist']):
        width = bar.get_width()
        ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2,
               f'{total/1e6:.1f}M', ha='left', va='center', fontweight='bold')
    
    # Format x-axis with millions
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1f}M'))
    
    plt.tight_layout()
    plt.savefig('visualizations/top_10_countries.png', dpi=300, bbox_inches='tight')
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
    
    ax.set_title('Top 10 Countries with Highest Growth (2011 vs 2024)', 
                fontweight='bold', pad=20)
    ax.set_xlabel('Growth Percentage (%)', fontweight='bold')
    ax.set_ylabel('Country', fontweight='bold')
    
    # Add percentage labels on bars (rounded, no decimals)
    for bar, pct in zip(bars, top_10_growth['growth_percentage']):
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2,
               f'{int(round(pct))}%', ha='left', va='center', fontweight='bold')
    
    # Add a vertical line at 0%
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('visualizations/top_10_highest_growth.png', dpi=300, bbox_inches='tight')
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
    plt.title('Monthly Distribution of Tourists as % of Annual Total', fontsize=20, fontweight='bold', pad=20)
    plt.xlabel('Month', fontsize=14, fontweight='bold')
    plt.ylabel('Year', fontsize=14, fontweight='bold')
    plt.xticks(fontsize=11, fontweight='bold')
    plt.yticks(fontsize=11, fontweight='bold')
    plt.tight_layout()
    plt.savefig('visualizations/monthly_distribution_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()


def animate_top_15_countries():
    # Prepare data: sum by year and country, EXCLUDING COVID YEARS (2020-2022)
    yearly_country = df[~df['year'].isin([2020, 2021, 2022])].groupby(['year', 'country'])['tourist'].sum().reset_index()
    
    # Pivot for bar_chart_race: index=year, columns=country, values=tourist
    pivot = yearly_country.pivot(index='year', columns='country', values='tourist').fillna(0)
    
    bcr.bar_chart_race(
        df=pivot,
        filename='visualizations/top_15_countries_barchart_race.mp4',
        orientation='h',
        sort='desc',
        n_bars=15,
        period_length=3000,  # Slower for smoother transitions (3 seconds per year)
        interpolate_period=True,
        title='Top 15 Countries by Tourism Visitors to Japan (1996-2024)\nExcluding Covid Era (2020-2022)',
        bar_size=.95,
        period_label=True,
        period_fmt='{x:.0f}',  # Show year as integer without decimal
        cmap='tab20',  # Use a pleasing colormap
        filter_column_colors=True,
        figsize=(16, 9),
        dpi=144,
        writer='ffmpeg',
        steps_per_period=30  # More frames for smoother animation
    )

# Main execution
if __name__ == "__main__":
    print("Creating visualizations...")
    
    # Create all visualizations
    plot_total_visitors_growth()
    print("Total visitors growth chart created")
    
    plot_regional_maps()
    print("Regional distribution stacked bar chart created")
    
    plot_top_countries()
    print("Top 10 countries chart created")
    
    plot_post_covid_growth()
    print("Post-COVID growth chart created")
    
    plot_monthly_distribution_heatmap()
    print("Monthly distribution heatmap created")
    
    animate_top_15_countries()
    print("Top 15 countries bar chart race animation created")
    
    print("\nAll visualizations saved in the 'visualizations' folder!") 