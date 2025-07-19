"""
Prefecture Visit Rate Visualization
Creates a choropleth map showing visit rates to different prefectures in Japan.
"""

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from plot_config import STANDARD_FIGURE_CONFIG, STANDARD_TITLE_CONFIG

def create_prefecture_choropleth():
    """Creates a choropleth map of prefecture visit rates in Japan."""
    
    # Load data
    df = pd.read_csv('raw_data/prefecture_visit_rate_2024.csv')
    top_10 = df.nlargest(10, 'Visit Rate(%)')
    gdf = gpd.read_file('shapefiles/gadm41_JPN_1.shp')
    
    # Map prefecture names to shapefile names
    name_mapping = {
        'Tokyo': 'Tokyo', 'Osaka': 'Osaka', 'Kyoto': 'Kyoto', 'Hokkaido': 'Hokkaido',
        'Chiba Prefecture': 'Chiba', 'Fukuoka Prefecture': 'Fukuoka', 'Nara Prefecture': 'Nara',
        'Yamanashi Prefecture': 'Yamanashi', 'Kanagawa Prefecture': 'Kanagawa', 'Aichi Prefecture': 'Aichi',
        'Hyogo Prefecture': 'Hyōgo', 'Okinawa Prefecture': 'Okinawa', 'Oita Prefecture': 'Oita',
        'Hiroshima Prefecture': 'Hiroshima', 'Gifu Prefecture': 'Gifu', 'Shizuoka Prefecture': 'Shizuoka',
        'Nagano Prefecture': 'Nagano', 'Ishikawa Prefecture': 'Ishikawa', 'Kumamoto Prefecture': 'Kumamoto',
        'Wakayama Prefecture': 'Wakayama', 'Tochigi Prefecture': 'Tochigi', 'Miyagi Prefecture': 'Miyagi',
        'Toyama Prefecture': 'Toyama', 'Kagawa Prefecture': 'Kagawa', 'Nagasaki Prefecture': 'Naoasaki',
        'Okayama Prefecture': 'Okayama', 'Saitama Prefecture': 'Saitama', 'Mie Prefecture': 'Mie',
        'Aomori Prefecture': 'Aomori', 'Saga Prefecture': 'Saga', 'Kagoshima prefecture': 'Kagoshima',
        'Yamagata Prefecture': 'Yamagata', 'Yamaguchi Prefecture': 'Yamaguchi', 'Niigata Prefecture': 'Niigata',
        'Shiga Prefecture': 'Shiga', 'Iwate Prefecture': 'Iwate', 'Gunma Prefecture': 'Gunma',
        'Ehime Prefecture': 'Ehime', 'Fukushima Prefecture': 'Fukushima', 'Miyazaki Prefecture': 'Miyazaki',
        'Akita Prefecture': 'Akita', 'Ibaraki Prefecture': 'Ibaraki', 'Tottori Prefecture': 'Tottori',
        'Tokushima Prefecture': 'Tokushima', 'Kochi Prefecture': 'Kochi', 'Fukui Prefecture': 'Fukui',
        'Shimane Prefecture': 'Shimane'
    }
    
    # Merge data
    df['Prefecture_Mapped'] = df['Prefecture'].map(name_mapping)
    gdf = gdf.merge(df, left_on='NAME_1', right_on='Prefecture_Mapped', how='left')
    
    # Create map
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    gdf.plot(column='Visit Rate(%)', ax=ax, cmap='Reds', legend=False, 
             missing_kwds={'color': 'lightgrey'}, edgecolor='black', linewidth=0.5)
    
    # Number positioning directions
    directions = [
        (1.2, -1.5), (1.5, -1.2), (1.5, -0.8), (-1.2, 1.5), (-1.8, 0.6),
        (-0.9, -1.2), (0.8, -1.8), (1.8, -0.9), (0, 0), (0.8, -1.8)
    ]
    
    # Add numbers and lines
    for i, (idx, row) in enumerate(top_10.iterrows(), 1):
        prefecture_geom = gdf[gdf['Prefecture'] == row['Prefecture']]
        if not prefecture_geom.empty:
            centroid = prefecture_geom.geometry.iloc[0].centroid
            direction = directions[i-1]
            
            if i == 9:
                # Number 9 inside prefecture
                ax.annotate(str(i), xy=(centroid.x, centroid.y), xytext=(0, 0), 
                           textcoords='offset points', fontsize=10, fontweight='bold', 
                           color='black', ha='center', va='center')
            else:
                # Numbers outside with connecting lines
                number_x = centroid.x + direction[0]
                number_y = centroid.y + direction[1]
                ax.plot([centroid.x, number_x], [centroid.y, number_y], 
                       color='black', linewidth=0.8, alpha=0.7)
                
                # Offset number position
                number_offset_x = number_x + (direction[0] * 0.15)
                number_offset_y = number_y + (direction[1] * 0.15)
                ax.annotate(str(i), xy=(number_offset_x, number_offset_y), xytext=(0, 0), 
                           textcoords='offset points', fontsize=10, fontweight='bold', 
                           color='black', ha='center', va='center')
    
    # Customize plot
    ax.set_title('Prefecture Visit Rates in Japan (2024)', **STANDARD_TITLE_CONFIG)
    ax.axis('off')
    
    # Add color bar
    sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=gdf['Visit Rate(%)'].min(), vmax=gdf['Visit Rate(%)'].max()))
    cbar = plt.colorbar(sm, ax=ax, orientation='vertical', shrink=0.8, pad=-0.2)
    cbar.set_label('Visit Rate (%)', fontsize=10)
    
    # Add legend
    ax.text(0.1, 0.98, "Top 10 Prefectures:", transform=ax.transAxes, 
            fontsize=16, verticalalignment='top', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.9))
    
    legend_list = ""
    for i, (idx, row) in enumerate(top_10.iterrows(), 1):
        visit_rate = float(row['Visit Rate(%)'])
        rounded_rate = round(visit_rate, 1)
        legend_list += f"{i}. {row['Prefecture']}: {rounded_rate}%\n"
    
    ax.text(0.1, 0.92, legend_list, transform=ax.transAxes, 
            fontsize=16, verticalalignment='top', fontweight='normal',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.9))
    
    plt.tight_layout()
    plt.savefig('visualizations/prefecture_visit_rate.png', **STANDARD_FIGURE_CONFIG)
    plt.show()
    
    print("Prefecture visit rate choropleth saved as 'visualizations/prefecture_visit_rate.png'")

if __name__ == "__main__":
    create_prefecture_choropleth() 