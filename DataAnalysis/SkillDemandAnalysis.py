import pandas as pd
import numpy as np
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
# Top 10 Skills
skills = {
    'Deutsch': ['German', 'Deutsch', 'Deutschkenntnisse'],
    'Englisch': ['English', 'Englisch'],
    'Kommunikation': ['Communication', 'Kommunikation'],
    'Flexibilität': ['Flexibility', 'Flexibilität'],
    'Innovation': ['Innovation', 'Innovationen'],
    'Weiterbildung': ['Continuing Education', 'Weiterbildung'],
    'Projektmanagement': ['Project Management', 'Projektmanagement'],
    'Programmierkenntnisse': ['Programming Skills', 'Programmierkenntnisse', 'Coding Skills', 'Coding'],
    'Kreativität': ['Creativity', 'Kreativität'],
    'Teamwork': ['Teamwork', 'Teamarbeit']
}


# Funktion zur Extraktion der Skills aus der Beschreibung
def extract_skills(description):
    skills_found = []
    for skill in skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', description, re.IGNORECASE):
            skills_found.append(skill)
    return skills_found

# Filtern der Daten auf die Top 15 Städte
filtered_data = data[data['search_location'].apply(lambda x: any(city in x for city in cities))].copy()

# Extrahieren der Skills und Städte aus der Beschreibung und dem Standort
filtered_data['skills'] = filtered_data['description'].apply(extract_skills)
filtered_data['city'] = filtered_data['search_location'].apply(lambda x: x.split(',')[0] if isinstance(x, str) else x)

# Explodieren der DataFrame nach Skills, um jeden Skill in einer neuen Zeile zu haben
exploded_data = filtered_data.explode('skills')

# Erstellung der Kreuztabelle
skills_city_df = pd.crosstab(exploded_data['city'], exploded_data['skills'])

# Berechnung der Korrelationsmatrix der Kreuztabelle
correlation_matrix = skills_city_df.corr()

# Visualisierung der Verteilung der Skills in den Top 15 Städten
plt.figure(figsize=(20, 12))
sns.heatmap(skills_city_df, cmap="PuBu", annot=True, fmt='d')
plt.title('Verteilung der Top 10 Skills in den Top 15 Städten', fontsize=20)
plt.xlabel('Skills', fontsize=16)
plt.ylabel('Städte', fontsize=16)
plt.xticks(rotation=45, ha='right', fontsize=14)
plt.yticks(rotation=0, ha='right', fontsize=14)
plt.subplots_adjust(bottom=0.2, left=0.2)
plt.show()

# Visualisierung der Korrelationsmatrix mit einer Heatmap
plt.figure(figsize=(20, 12))
sns.heatmap(correlation_matrix, cmap="coolwarm", annot=True, fmt='.2f')
plt.title('Korrelationen zwischen Skills', fontsize=20)
plt.xlabel('Skills', fontsize=16)
plt.ylabel('Skills', fontsize=16)
plt.xticks(rotation=45, ha='right', fontsize=14)
plt.yticks(rotation=0, ha='right', fontsize=14)
plt.subplots_adjust(bottom=0.2, left=0.2)
plt.show()
