# Tourism trends in Japan
Analyzing tourism trends for Japan using public datasets, geospatial data, and custom visualizations.

## Table of Contents

1. [Overview](#overview)
2. [Articles / Publications](#articles--publications)
3. [Project Workflow](#project-workflow)
4. [File Structure](#file-structure)
5. [Data Directory](#data-directory)
6. [Visualizations / Outputs](#visualizations--outputs)
7. [Key Concepts / Variables](#key-concepts--variables)
8. [Installation and Setup](#installation-and-setup)
9. [Usage](#usage)
10. [Results / Interpretation](#results--interpretation)
11. [Technical Details](#technical-details)
12. [Dependencies](#dependencies)
13. [Notes / Limitations](#notes--limitations)

---

## Overview

* **Goal**: Provide a clear, data-driven view of Japan’s inbound tourism trends, regional distribution, spending, and cultural drivers.
* **Approach**: Data cleaning and transformation with pandas, statistical summaries, geospatial mapping with GeoPandas, and rich visualizations in Matplotlib/Seaborn; animation with `bar_chart_race`.
* **Highlights**:
  - Unified plotting style via `plot_config.py` for consistent visuals.
  - Multiple perspectives: macro growth, country mix, seasonality, regional map, spend, and cultural exports.
  - Reproducible scripts that output PNGs, MP4, and GIFs under `visualizations/`.

---

## Articles / Publications

* Medium: https://medium.com/@ritu.bansalrb00/why-is-everyone-going-to-japan-34815b9b7247

---

## Project Workflow

1. **Data Collection / Extraction**: CSVs curated under `raw_data/` and Japan GADM shapefiles under `shapefiles/`.
2. **Data Preprocessing / Cleaning**: `clean_visitors_csv.py` reshapes multi-index visitor data, maps countries to regions, and standardizes numeric columns.
3. **Modeling / Analysis**: Aggregations for YoY and regional shares; growth comparisons across countries and periods.
4. **Evaluation / Validation**: Sanity checks (exclusion of 2020–2022 for reliability), manual inspection of outputs.
5. **Visualization / Reporting**: Static charts, heatmaps, choropleth maps, and animated race charts saved to `visualizations/`.

---

## File Structure

### Core Scripts

#### `plot_config.py`
* Purpose: Centralized styling (fonts, sizes, colors, grids) for all plots.
* Input: N/A (imported by other scripts).
* Output: N/A.
* Key Features: `COLOR_PALETTE`, `STANDARD_TITLE_CONFIG`, `STANDARD_LABEL_CONFIG`, `STANDARD_GRID_CONFIG`, `STANDARD_FIGURE_CONFIG`.

#### `clean_visitors_csv.py`
* Purpose: Convert multi-level CSV of inbound visitors into a clean, tidy format.
* Input: `raw_data/Visitors_by_nationality.csv`
* Output: Writes `processed_data/cleaned_visitors.csv` (script default). Note: a `raw_data/cleaned_visitors.csv` is present in this repo and is used by downstream scripts.
* Key Features: Country→region mapping; melt+pivot; numeric cleaning; column standardization to `year, month, country, region, total, tourist, business, others, short_excursion`.

#### `visualize_tourism_growth.py`
* Purpose: Produce multiple macro-level visuals and animations.
* Input: `raw_data/cleaned_visitors.csv`, `raw_data/tourism_top_10_countries.csv`
* Output: PNGs and animations in `visualizations/`:
  - `total_visitors_growth.png`
  - `top_10_countries.png`
  - `top_10_highest_growth.png`
  - `monthly_distribution_heatmap.png`
  - `top_15_countries_barchart_race.mp4` and `.gif`
  - `two_period_growth_comparison.png`
  - `stacked_region_distribution.png`
* Key Features: Excludes 2020–2022 where relevant; custom palette; bar-chart race via `bar_chart_race`.

#### `travel_costs.py`
* Purpose: Visualize CPI-adjusted daily travel costs by country and compute total yearly spend by tourists in Japan.
* Input: `raw_data/travel_costs.csv`, `raw_data/spend_per_capita.csv`, `raw_data/cleaned_visitors.csv`
* Output: `visualizations/travel_costs_cpi_adjusted.png`, `visualizations/total_yearly_spend_usd.png`
* Key Features: Cleans currency formatting; merges visitor volumes with per-capita spend; converts JPY→USD using fixed yearly averages; excludes 2020–2022 for reliability.

#### `cultural_exports.py`
* Purpose: Chart market size and growth for anime and manga; track adoption via sushi restaurants in the USA.
* Input: `raw_data/Anime_market_stats.csv`, `raw_data/Manga_market_stats .csv`, `raw_data/sushi_restaurants_in_USA.csv`
* Output: `visualizations/anime_market_growth.png`, `visualizations/manga_market_growth.png`, `visualizations/sushi_restaurants_growth.png`
* Key Features: Numeric cleaning and unit conversion to USD billions; consistent styling.

#### `visit_motivation.py`
* Purpose: Rank top activities tourists did in Japan (2024).
* Input: `raw_data/purpose_of_visit_2024.csv`
* Output: `visualizations/visit_motivation.png`
* Key Features: Filters survey item, sorts by composition ratio, annotates horizontal bars.

#### `prefecture_visit_rate.py`
* Purpose: Choropleth map of top prefecture visit rates with callouts.
* Input: `raw_data/prefecture_visit_rate_2024.csv`, `shapefiles/gadm41_JPN_1.*`
* Output: `visualizations/prefecture_visit_rate.png`
* Key Features: Prefecture name mapping to shapefile labels; top-10 numbering and connectors; colorbar and legend overlay.

---

## Data Directory

The project uses the following directories:

* `raw_data/`
  - Visitors and metadata CSVs: `Visitors_by_nationality.csv`, `cleaned_visitors.csv`, `tourism_top_10_countries.csv`, `travel_costs.csv`, `spend_per_capita.csv`, `purpose_of_visit_2024.csv`, `prefecture_visit_rate_2024.csv`, `Anime_market_stats.csv`, `Manga_market_stats .csv`, `sushi_restaurants_in_USA.csv`.
* `shapefiles/`
  - GADM Japan boundaries at levels 0/1/2: `gadm41_JPN_*.{shp,shx,dbf,prj,cpg}`.
* `processed_data/` (optional)
  - Created by `clean_visitors_csv.py` when run as-is to store `cleaned_visitors.csv`.

---

## Visualizations / Outputs

Static and animated outputs are saved to `visualizations/`:

* Static PNGs: `total_visitors_growth.png`, `top_10_countries.png`, `top_10_highest_growth.png`, `monthly_distribution_heatmap.png`, `stacked_region_distribution.png`, `travel_costs_cpi_adjusted.png`, `total_yearly_spend_usd.png`, `anime_market_growth.png`, `manga_market_growth.png`, `sushi_restaurants_growth.png`, `visit_motivation.png`, `prefecture_visit_rate.png`.
* Animations: `top_15_countries_barchart_race.mp4`, `top_15_countries_barchart_race.gif`.

---

## Key Concepts / Variables

* Visitor dataset standardized columns: `year`, `month`, `country`, `region`, `total`, `tourist`, `business`, `others`, `short_excursion`.
* Regions derived from country mapping (e.g., Asia, Europe, North America, Oceania, South America, Africa).
* Choropleth uses prefecture-level visit rates (`Visit Rate(%)`).

---

## Installation and Setup

1. Clone repository
   ```bash
   git clone <repository-url>
   cd japan_tourism
   ```

2. Install Python dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. System tools for animations (optional, for MP4/GIF)
   - MP4 writer: `ffmpeg`
   - GIF writer: `ImageMagick`

4. Data placement
   - Ensure CSVs exist under `raw_data/` and shapefiles under `shapefiles/`.

---

## Usage

### Run Complete Visualization Suite
```bash
python visualize_tourism_growth.py
python travel_costs.py
python cultural_exports.py
python visit_motivation.py
python prefecture_visit_rate.py
```

### Run Preprocessing Only
```bash
python clean_visitors_csv.py  # writes processed_data/cleaned_visitors.csv
```

### Use Components Programmatically
```python
from prefecture_visit_rate import create_prefecture_choropleth

create_prefecture_choropleth()
```

All outputs will be saved under `visualizations/`.

---

## Results / Interpretation

* Macro-level inbound growth and seasonality shown via line charts and heatmaps.
* Mix by origin and growth since 2011 highlighted in top-10 bar charts.
* Regional distribution visualized as a prefecture-level choropleth.
* Spending trends summarized via CPI-adjusted costs and total yearly USD spend.

See figures in `visualizations/` for details.

---

## Technical Details

* Frameworks / Tools: pandas, NumPy, Matplotlib, Seaborn, GeoPandas, Fiona, bar_chart_race.
* Styling centralized in `plot_config.py` for consistent typography, palette, and grids.
* Implementation notes: exclusions for 2020–2022 in some analyses; fixed JPY→USD yearly averages for spend conversion.

---

## Dependencies

See `requirements.txt`:

* pandas
* numpy
* matplotlib
* seaborn
* bar_chart_race
* geopandas==0.12.2
* fiona==1.8.22

---

## Notes / Limitations

* Some visuals explicitly exclude 2020–2022 due to pandemic-era distortions.
* Prefecture name mapping is manual and may require updates for alternate spellings.
* `clean_visitors_csv.py` writes to `processed_data/` by default, whereas downstream scripts read `raw_data/cleaned_visitors.csv`. Adjust paths as needed.
* `Manga_market_stats .csv` filename includes a space before `.csv` and is referenced as-is.