import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensure visualizations folder exists
if not os.path.exists('visualizations'):
    os.makedirs('visualizations')

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
    plt.xlabel('Participation Rate', fontsize=14)
    plt.title('Top 10 Activities Tourists Did During Their Stay in Japan (2024)', fontsize=18, pad=20)
    plt.tight_layout()
    for bar, value in zip(bars, top_10_data['Composition ratio'][::-1]):
        plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{value:.0f}%', va='center', fontsize=12)
    plt.savefig('visualizations/visit_motivation.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Bar chart saved as 'visualizations/visit_motivation.png'")

if __name__ == "__main__":
    plot_visit_motivation()