"""
Standardized plotting configuration for Japan Tourism visualizations.
This module provides consistent font, size, and formatting settings across all charts.
"""

import matplotlib.pyplot as plt

# Set up standardized fonts
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Georgia']
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 18
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['figure.titlesize'] = 20

# Standardized formatting configuration
STANDARD_FONT_CONFIG = {
    'fontfamily': 'serif',
    'fontsize': 12,
    'fontweight': 'normal'
}

STANDARD_TITLE_CONFIG = {
    'fontsize': 18,
    'fontweight': 'bold',
    'pad': 20
}

STANDARD_LABEL_CONFIG = {
    'fontsize': 14,
    'fontweight': 'bold'
}

STANDARD_TICK_CONFIG = {
    'fontsize': 12,
    'fontweight': 'normal'
}

# Custom divergent color palette (expanded to 10 colors)
COLOR_PALETTE = [
    '#2066a8',  # Dark Blue
    '#3a7fc2',  # Between Dark & Med Blue
    '#8ec1da',  # Med Blue
    '#a7d3e4',  # Between Med & Light Blue
    '#cde1ec',  # Light Blue
    '#ededed',  # Gray
    '#f6d6c2',  # Light Red
    '#efb09a',  # Between Light & Med Red
    '#d47264',  # Med Red
    '#ae282c'   # Dark Red
]

# Standard figure settings
STANDARD_FIGURE_CONFIG = {
    'dpi': 300,
    'bbox_inches': 'tight'
}

# Standard grid settings
STANDARD_GRID_CONFIG = {
    'alpha': 0.3,
    'linestyle': '--'
} 