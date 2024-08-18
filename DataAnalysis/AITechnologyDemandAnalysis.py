import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Lesen der CSV-Datei
file_path = '../Daten/cleaned_merged_final.csv'
data = pd.read_csv(file_path)

# Top 15 Städte
cities = [
    'Berlin', 'München', 'Hamburg', 'Frankfurt', 'Düsseldorf', 'Köln', 'Stuttgart',
    'Hannover', 'Leipzig', 'Essen', 'Nürnberg', 'Dortmund', 'Münster', 'Karlsruhe',
]

# Top 10 AI-Technologien
technologies = [
    'Python', 'R', 'SQL', 'MS', 'Azure', 'AWS', 'Java', 'DevOps', 'Go', 'Docker'
]

# Funktion zur Extraktion der Technologien aus der Beschreibung
def extract_technologies(description):
    technologies_found = []
    for tech in technologies:
        if re.search(r'\b' + re.escape(tech) + r'\b', description, re.IGNORECASE):
            technologies_found.append(tech)
    return technologies_found

# Filtern der Daten auf die Top 15 Städte
filtered_data = data[data['search_location'].apply(lambda x: any(city in x for city in cities))].copy()

# Extrahieren der AI-Technologien und Städte aus der Beschreibung und dem Standort
filtered_data['technologies'] = filtered_data['description'].apply(extract_technologies)
filtered_data['city'] = filtered_data['search_location'].apply(lambda x: x.split(',')[0] if isinstance(x, str) else x)

# Explodieren der DataFrame nach Technologien, um jede Technologie in einer neuen Zeile zu haben
exploded_data = filtered_data.explode('technologies')

# Erstellung der Kreuztabelle
tech_city_df = pd.crosstab(exploded_data['city'], exploded_data['technologies'])

# Berechnung der Korrelationsmatrix der Kreuztabelle
correlation_matrix = tech_city_df.corr()

# Visualisierung der Verteilung der AI-Technologien in den Top 15 Städten
plt.figure(figsize=(18, 10))
sns.heatmap(tech_city_df, cmap="PuBu", annot=True, fmt='d')
plt.title('Verteilung der Top 10 Technologien in den Top 15 Städten')
plt.xlabel('AI-Technologien')
plt.ylabel('Städte')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.show()

# Visualisierung der Korrelationsmatrix mit einer Heatmap
plt.figure(figsize=(18, 10))
sns.heatmap(correlation_matrix, cmap="coolwarm", annot=True, fmt='.2f')
plt.title('Korrelationen zwischen Technologien')
plt.xlabel('Technologien')
plt.ylabel('Technologien')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.show()
