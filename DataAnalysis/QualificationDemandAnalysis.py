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

# Liste von Qualifikationen
qualifications = {
    'Informatik': ['Informatik', 'Computer Science', 'Computer Sciences', 'Informatics'],
    'Mathematik': ['Mathematik', 'Mathematics'],
    'Wirtschaftswissenschaften': ['Wirtschaftswissenschaften', 'Economics', 'Economic Sciences'],
    'Data Science': ['Data Science', 'Datenwissenschaft', 'Data Sciences'],
    'Künstliche Intelligenz': ['Artificial Intelligence', 'Künstliche Intelligenz', 'AI', 'KI'],
    'Wirtschaftsinformatik': ['Wirtschaftsinformatik', 'Business Informatics'],
    'BWL': ['Business Administration', 'Betriebswirtschaftslehre', 'BWL'],
    'Physik': ['Physics', 'Physik'],
    'Statistik': ['Statistics', 'Statistik'],
    'Elektrotechnik': ['Electrical Engineering', 'Elektrotechnik', 'Electrical and Electronic Engineering']
}


# Funktion zur Extraktion der Qualifikationen aus der Beschreibung
def extract_qualifications(description):
    qualifications_found = []
    for qual in qualifications:
        if re.search(r'\b' + re.escape(qual) + r'\b', description, re.IGNORECASE):
            qualifications_found.append(qual)
    return qualifications_found

# Filtern der Daten auf die Top 15 Städte
filtered_data = data[data['search_location'].apply(lambda x: any(city in x for city in cities))].copy()

# Extrahieren der Qualifikationen und Städte aus der Beschreibung und dem Standort
filtered_data['qualifications'] = filtered_data['description'].apply(extract_qualifications)
filtered_data['city'] = filtered_data['search_location'].apply(lambda x: x.split(',')[0] if isinstance(x, str) else x)

# Explodieren der DataFrame nach Qualifikationen, um jede Qualifikation in einer neuen Zeile zu haben
exploded_data = filtered_data.explode('qualifications')

# Erstellung der Kreuztabelle
qual_city_df = pd.crosstab(exploded_data['city'], exploded_data['qualifications'])

# Berechnung der Korrelationsmatrix der Kreuztabelle
correlation_matrix = qual_city_df.corr()

# Heatmap für die Verteilung der Qualifikationen
plt.figure(figsize=(20, 12))
sns.heatmap(qual_city_df, cmap="PuBu", annot=True, fmt='d')
plt.title('Verteilung der Qualifikationen in den Top 15 deutschen Städten', fontsize=20)
plt.xlabel('Qualifikationen', fontsize=16)
plt.ylabel('Städte', fontsize=16)
plt.xticks(rotation=45, ha='right', fontsize=14)
plt.yticks(rotation=0, ha='right', fontsize=14)
plt.subplots_adjust(bottom=0.2, left=0.2)
plt.show()

# Heatmap für die Korrelationsanalyse
plt.figure(figsize=(20, 12))
sns.heatmap(correlation_matrix, cmap="coolwarm", annot=True, fmt='.2f')
plt.title('Korrelationen zwischen Qualifikationen', fontsize=20)
plt.xlabel('Qualifikationen', fontsize=16)
plt.ylabel('Qualifikationen', fontsize=16)
plt.xticks(rotation=45, ha='right', fontsize=14)
plt.yticks(rotation=0, ha='right', fontsize=14)
plt.subplots_adjust(bottom=0.2, left=0.2)
plt.show()
