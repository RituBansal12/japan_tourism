import pandas as pd

# Country to region mapping (add more as needed)
country_region = {
    # Asia
    'Korea': 'Asia', 'China': 'Asia', 'Taiwan': 'Asia', 'Hong Kong': 'Asia', 'Thailand': 'Asia', 'Singapore': 'Asia', 'Malaysia': 'Asia', 'Indonesia': 'Asia', 'Philippines': 'Asia', 'Vietnam': 'Asia', 'India': 'Asia', 'Middle East': 'Asia', 'Israel': 'Asia', 'Turkey': 'Asia', 'GCC': 'Asia', 'Macau': 'Asia', 'Mongolia': 'Asia', 'Asia Unclassified': 'Asia',
    # Europe
    'United Kingdom': 'Europe', 'France': 'Europe', 'Germany': 'Europe', 'Italy': 'Europe', 'Russia': 'Europe', 'Spain': 'Europe', 'Sweden': 'Europe', 'Netherland': 'Europe', 'Swiss': 'Europe', 'Belgium': 'Europe', 'Finland': 'Europe', 'Poland': 'Europe', 'Denmark': 'Europe', 'Norway': 'Europe', 'Austria': 'Europe', 'Portugal': 'Europe', 'Ireland': 'Europe', 'Europe Unclassified': 'Europe',
    # Africa
    'Africa': 'Africa',
    # North America
    'U.S.A.': 'North America', 'Canada': 'North America', 'Mexico': 'North America', 'North America Unclassified': 'North America',
    # South America
    'Brazil': 'South America', 'South America Unclassified': 'South America',
    # Oceania
    'Australia': 'Oceania', 'New Zealand': 'Oceania', 'Oceania Unclassified': 'Oceania',
}

def get_region(country):
    return country_region.get(country, 'Other')

# Read the CSV with multi-level columns (first row: country, second row: category)
df = pd.read_csv('raw_data/Visitors_by_nationality.csv', header=[0, 1])

# Use the actual column names from the CSV
id_vars = [('Unnamed: 0_level_0', 'Year'), ('Country', 'Month')]
value_vars = [col for col in df.columns if col not in id_vars]

df_long = df.melt(id_vars=id_vars, value_vars=value_vars, var_name=['country', 'category'], value_name='visitors')

# Pivot so each row is year, month, country, and columns for each category
df_pivot = df_long.pivot_table(index=[('Unnamed: 0_level_0', 'Year'), ('Country', 'Month'), 'country'], columns='category', values='visitors', aggfunc='first').reset_index()

# Rename columns to match the required output
df_pivot.columns.name = None
column_map = {
    ('Unnamed: 0_level_0', 'Year'): 'year',
    ('Country', 'Month'): 'month',
    'country': 'country',
    'Total': 'total',
    'Tourist': 'tourist',
    'Business': 'business',
    'Others': 'others',
    'Short Excursion': 'short_excursion',
}
df_pivot = df_pivot.rename(columns=column_map)

# Add region column after country
regions = df_pivot['country'].apply(get_region)
df_pivot.insert(df_pivot.columns.get_loc('country') + 1, 'region', regions)

# Reorder columns
final_columns = ['year', 'month', 'country', 'region', 'total', 'tourist', 'business', 'others', 'short_excursion']
df_pivot = df_pivot[final_columns]

# Clean up the numeric columns: remove commas, convert to int, handle missing values
for col in ['total', 'tourist', 'business', 'others', 'short_excursion']:
    df_pivot[col] = (
        df_pivot[col]
        .astype(str)
        .str.replace(',', '', regex=False)
        .replace({'': None, 'nan': None})
        .astype(float)
        .round(0)
        .astype('Int64')
    )

# Write to CSV
df_pivot.to_csv('raw_data/cleaned_visitors.csv', index=False)

print('Cleaned data written to raw_data/cleaned_visitors.csv') 