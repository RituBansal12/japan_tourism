import pandas as pd
import matplotlib.pyplot as plt
import os

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

# File paths
anime_path = os.path.join('raw_data', 'Anime_market_stats.csv')
manga_path = os.path.join('raw_data', 'Manga_market_stats .csv')  # Note the space in the filename
sushi_path = os.path.join('raw_data', 'sushi_restaurants_in_USA.csv')

# --- Anime Market Visualization ---
anime_df = pd.read_csv(anime_path)
anime_df['Domestic(USD Million)'] = anime_df['Domestic(USD Million)'].replace({'[$,]': '', '"': ''}, regex=True).astype(float)
anime_df['Overseas(USD Million)'] = anime_df['Overseas(USD Million)'].replace({'[$,]': '', '"': ''}, regex=True).astype(float)
anime_df['Year'] = anime_df['Year'].astype(int)

# Convert to USD Billion
anime_df['Domestic(USD Billion)'] = anime_df['Domestic(USD Million)'] / 1000
anime_df['Overseas(USD Billion)'] = anime_df['Overseas(USD Million)'] / 1000

plt.figure(figsize=(10, 6))
plt.plot(anime_df['Year'], anime_df['Domestic(USD Billion)'], label='Domestic Market Size (USD Billion)', marker='o', color=COLOR_PALETTE[0])
plt.plot(anime_df['Year'], anime_df['Overseas(USD Billion)'], label='Overseas Market Size (USD Billion)', marker='o', color=COLOR_PALETTE[9])
plt.title('Anime Market Growth (Domestic vs Overseas)')
plt.xlabel('Year')
plt.ylabel('Market Size (USD Billion)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(anime_df['Year'], rotation=90)
plt.tight_layout()
plt.savefig('visualizations/anime_market_growth.png')
plt.show()

# --- Manga Market Visualization ---
manga_df = pd.read_csv(manga_path)
manga_df['Total Market(USD Million)'] = manga_df['Total Market(USD Million)'].replace({'[$,]': '', '"': ''}, regex=True).astype(float)
manga_df['Year'] = manga_df['Year'].astype(int)
# Convert to USD Billion
manga_df['Total Market(USD Billion)'] = manga_df['Total Market(USD Million)'] / 1000

plt.figure(figsize=(10, 6))
plt.plot(manga_df['Year'], manga_df['Total Market(USD Billion)'], label='Market Size (USD Billion)', color=COLOR_PALETTE[0], marker='o')
plt.title('Manga Market Growth (Forecast)')
plt.xlabel('Year')
plt.ylabel('Market Size (USD Billion)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(manga_df['Year'], rotation=90)
plt.tight_layout()
plt.savefig('visualizations/manga_market_growth.png')
plt.show()

# --- Sushi Restaurants in USA Visualization ---
sushi_df = pd.read_csv(sushi_path)
sushi_df['Year'] = sushi_df['Year'].astype(int)
sushi_df['num_businesses'] = sushi_df['num_businesses'].astype(int)

plt.figure(figsize=(10, 6))
plt.plot(sushi_df['Year'], sushi_df['num_businesses'], label='Number of Restaurants', color=COLOR_PALETTE[9], marker='o')
plt.title('Growth of Sushi Restaurants in USA')
plt.xlabel('Year')
plt.ylabel('Number of Businesses')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(sushi_df['Year'], sushi_df['Year'], rotation=90)
plt.tight_layout()
plt.savefig('visualizations/sushi_restaurants_growth.png')
plt.show() 