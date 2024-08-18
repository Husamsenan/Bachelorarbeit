import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Laden der Städte-Liste aus der CSV-Datei
# Quelle der Datei: https://github.com/andrena/java8-workshop/blob/master/demos/Liste-Staedte-in-Deutschland.csv
cities_file_path = '../Liste-Staedte-in-Deutschland.csv'
cities_data = pd.read_csv(cities_file_path, on_bad_lines='skip', sep=';')
cities = cities_data['Stadt'].dropna().tolist()

# Sicherstellen, dass alle Vorkommen von "Frankfurt" als eine Stadt gezählt werden
cities = ['Frankfurt' if 'Frankfurt' in city else city for city in cities]

# Laden der Hauptdaten CSV-Datei
file_path = '../Daten/cleaned_merged_final.csv'  # Ersetzen Sie dies durch den korrekten Pfad zu Ihrer Datei
data = pd.read_csv(file_path)

# Zählen der Vorkommen jeder Stadt in der Spalte 'job_location' mit genauer Übereinstimmung
city_counts = {city: data['job_location'].str.contains(r'\b{}\b'.format(city), case=False, na=False).sum() for city in cities}

# Zusammenfassen aller Zählungen für "Frankfurt"
city_counts['Frankfurt'] = sum(count for city, count in city_counts.items() if 'Frankfurt' in city)

# Entfernen von Duplikaten, falls vorhanden (nur "Frankfurt" beibehalten)
city_counts = {city: count for city, count in city_counts.items() if city != 'Frankfurt (Oder)'}

# Erstellen eines DataFrames aus den Ergebnissen und Filtern nach Städten mit mindestens 1 Job
city_counts_df = pd.DataFrame(list(city_counts.items()), columns=['Stadt', 'Anzahl_Jobs'])
city_counts_df = city_counts_df[city_counts_df['Anzahl_Jobs'] > 0]

# Speichern des DataFrames als CSV-Datei mit allen Städten, die mindestens 1 Job haben
output_file_path = '../Tables/staedte_job_anzahl.csv'
city_counts_df.to_csv(output_file_path, index=False)

# Sortieren nach der Anzahl der Jobs für die Top 15 Städte
city_counts_df = city_counts_df.sort_values(by='Anzahl_Jobs', ascending=False)

# Top 15 Städte auswählen
top_15_cities_filtered = city_counts_df.head(15).values.tolist()

# Farben für die Balken definieren
colors = plt.cm.tab20(np.linspace(0, 1, len(top_15_cities_filtered)))

# Plot der Top 15 Städte
plt.figure(figsize=(10, 6))
bars = plt.bar([city[0] for city in top_15_cities_filtered], [city[1] for city in top_15_cities_filtered], color=colors)
plt.xlabel('Stadt')
plt.ylabel('Anzahl der KI Stellenanzeigen')
plt.title('Top 15 Städte nach Anzahl der KI Stellenanzeigen')
plt.xticks(rotation=45, ha='right')

# Werte oben auf den Balken anzeigen
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom', ha='center')

plt.tight_layout()
plt.show()

# Ausgabe der gesamten Liste in der Konsole
for city, count in city_counts_df.values.tolist():
    print(f"{city}: {count}")
