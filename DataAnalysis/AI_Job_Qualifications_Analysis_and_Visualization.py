import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np

# Datei einlesen
file_path = '../Daten/cleaned_merged_final.csv'
data = pd.read_csv(file_path)

# Überprüfen der ersten paar Zeilen der 'description'-Spalte
print("Erste paar Beschreibungen:")
print(data['description'].head())

# Gesamtanzahl der Zeilen überprüfen
print(f"\nGesamtanzahl der Zeilen: {len(data)}")

# Gruppen von verwandten Qualifikationen
qualification_groups = {
    'Informatik': ['Informatik', 'Computer Science'],
    'Mathematik': ['Mathematik', 'Mathematics'],
    'Data Science': ['Data Science', 'Datenwissenschaft'],
    'Künstliche Intelligenz': ['Artificial Intelligence', 'Künstliche Intelligenz'],
    'Statistik': ['Statistics', 'Statistik'],
    'Physik': ['Physics', 'Physik'],
    'Elektrotechnik': ['Electrical Engineering', 'Elektrotechnik'],
    'Wirtschaftswissenschaften': ['Economics', 'Wirtschaftswissenschaften'],
    'Operations Research': ['Operations Research'],
    'Wirtschaftsinformatik': ['Wirtschaftsinformatik', 'Business Informatics'],
    'Bauingenieurwesen': ['Bauingenieurwesen', 'Civil Engineering'],
    'Ingenieurwissenschaften': ['Engineering Sciences', 'Ingenieurwissenschaften'],
    'BWL': ['Business Administration', 'Betriebswirtschaftslehre', 'BWL'],
    'Elektronik': ['Electrical', 'Elektronik'],
    'Informationstechnik': ['Information Engineering', 'Informationstechnik'],
    'Robotik': ['Robotics', 'Robotik'],
    'Bioinformatik': ['Bioinformatics', 'Bioinformatik'],
    'Ingenieurinformatik': ['Engineering Informatics', 'Ingenieurinformatik'],
    'Cybersicherheit': ['Cybersecurity', 'Cybersicherheit'],
    'Mechatronik': ['Mechatronik', 'Mechatronics']
}

# Zählen der Vorkommen jeder Gruppe
group_counts = {group_name: 0 for group_name in qualification_groups}
unique_descriptions = pd.Series(False, index=data.index)

# Initialisieren eines DataFrame für die Zählung jeder Qualifikation in den Beschreibungen
qual_counts_per_description = pd.DataFrame(0, index=data.index, columns=qualification_groups.keys())

for group_name, terms in qualification_groups.items():
    # Escape special characters in terms for regex
    escaped_terms = [re.escape(term) for term in terms]
    # Kombinierte Bedingung für die Gruppe erstellen
    combined_condition = data['description'].str.contains(fr'(?i)\b(?:{"|".join(escaped_terms)})\b', case=False, regex=True)
    # Zählen der Vorkommen jeder Qualifikation pro Beschreibung
    qual_counts_per_description.loc[combined_condition, group_name] = 1
    # Gesamtzahl der einzigartigen Vorkommen der Gruppe
    group_counts[group_name] = combined_condition.sum()
    # Aktualisiere die Gesamtheit der Beschreibungen, die mindestens eine Qualifikation enthalten
    unique_descriptions = unique_descriptions | combined_condition

# Gesamtergebnis der Beschreibungen, die mindestens eine Qualifikation enthalten
unique_count_all = unique_descriptions.sum()

# Summiere die Anzahl der Qualifikationen pro Gruppe
final_group_counts = qual_counts_per_description.sum()

# Erstellen eines DataFrames aus den Ergebnissen und Sortieren nach Vorkommen
group_counts_df = final_group_counts.to_frame(name='count').sort_values(by='count', ascending=False)

# Alle Qualifikationen anzeigen
print("\nVorkommen aller Qualifikationen in den Jobbeschreibungen:")
print(group_counts_df)

# Top 10 Qualifikationen anzeigen
top_10_groups = group_counts_df.head(10)

# Ergebnisse ausgeben
print("\nTop 10 Qualifikationen in den Jobbeschreibungen:")
print(top_10_groups)

print(f"\nGesamtanzahl der Beschreibungen, die mindestens eine der Qualifikationen enthalten: {unique_count_all}")

# Funktion zum Erstellen eines Balkendiagramms
def create_bar_chart(data, title, x_label, y_label, x_ticks_rotation=0):
    plt.figure(figsize=(12, 8))

    # Farben aus der tab20 Palette zuweisen
    tab20_colors = plt.cm.tab20(np.linspace(0, 1, len(data)))

    bars = plt.bar(data.index, data['count'], color=tab20_colors)
    plt.title(title, fontsize=14)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.xticks(ticks=np.arange(len(data.index)), labels=data.index, rotation=x_ticks_rotation, fontsize=10, ha='right')
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7)

    # Werte oben auf die Balken schreiben
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, int(yval), ha='center', fontsize=10)

    plt.tight_layout()
    plt.show()

# Balkendiagramm für die Top 10 Qualifikationen
create_bar_chart(top_10_groups, 'Top 10 Qualifikationen in den Jobbeschreibungen', 'Qualifikation', 'Anzahl', x_ticks_rotation=45)