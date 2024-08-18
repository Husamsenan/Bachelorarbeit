import pandas as pd
from bs4 import BeautifulSoup

# Function to remove HTML tags
def remove_html_tags(text):
    return BeautifulSoup(text, 'html.parser').get_text() if pd.notnull(text) else text

# Load and clean stepstone_final.csv
try:
    df_stepstone = pd.read_csv('stepstone_jobs_final.csv', encoding='utf-8')
except UnicodeDecodeError:
    df_stepstone = pd.read_csv('stepstone_jobs_final.csv', encoding='ISO-8859-1')

df_stepstone['description'] = df_stepstone['description'].apply(remove_html_tags)

# Load and clean indeed_final.csv
try:
    df_indeed = pd.read_csv('indeed_jobs_final.csv', encoding='utf-8')
except UnicodeDecodeError:
    df_indeed = pd.read_csv('indeed_jobs_final.csv', encoding='ISO-8859-1')

df_indeed['description'] = df_indeed['description'].apply(remove_html_tags)

# Merge the two DataFrames
df_merged = pd.concat([df_stepstone, df_indeed], ignore_index=True)

# Remove duplicate rows
df_merged = df_merged.drop_duplicates()

# Save the merged DataFrame to a new CSV file
df_merged.to_csv('merged_final_cleaned.csv', index=False)

# Print the first 10 rows of the merged 'description' column to check
print(df_merged['description'].head(10))
