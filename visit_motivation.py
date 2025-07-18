import pandas as pd
import matplotlib.pyplot as plt
import os
from plot_config import *

# Ensure visualizations folder exists
if not os.path.exists('visualizations'):
    os.makedirs('visualizations')

def plot_visit_motivation():
    df = pd.read_csv('raw_data/purpose_of_visit_2024.csv')
    filtered_df = df[df['Item2'] == 'What did you do during your current stay in Japan?']
    filtered_df = filtered_df.sort_values('Composition ratio', ascending=False)
    top_10_data = filtered_df.head(10).reset_index(drop=True)

    plt.figure(figsize=(12, 7))
    bars = plt.barh(
        top_10_data['Item1'][::-1],  # reverse for descending order
        top_10_data['Composition ratio'][::-1],
        color=COLOR_PALETTE[::-1],  # reverse so grey is in the middle visually
        alpha=0.85,
        edgecolor='black' 
    )
    plt.xlabel('Participation Rate', **STANDARD_LABEL_CONFIG)
    plt.title('Top 10 Activities Tourists Did During Their Stay in Japan (2024)', **STANDARD_TITLE_CONFIG)
    plt.tight_layout()
    for bar, value in zip(bars, top_10_data['Composition ratio'][::-1]):
        plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{value:.0f}%', va='center', fontsize=12, fontweight='bold')
    plt.savefig('visualizations/visit_motivation.png', **STANDARD_FIGURE_CONFIG)
    plt.close()
    print("Bar chart saved as 'visualizations/visit_motivation.png'")

if __name__ == "__main__":
    plot_visit_motivation()