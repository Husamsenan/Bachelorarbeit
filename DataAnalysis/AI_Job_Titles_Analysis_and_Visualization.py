import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Laden der Daten
file_path = '../Daten/cleaned_merged_final.csv'  # Bitte passe den Pfad zu deiner Datei an
data = pd.read_csv(file_path)

# Funktion zum Vereinfachen und Gruppieren von Jobtiteln
def simplify_title_v5(title):
    prefixes = ['Duales Studium', 'm/w/d', 'w/m/d', 'w|m|d', 'w|m', 'm|w|d', 'Senior', 'Junior', '(Junior)', 'Lead', 'Principal',
                'Chief', 'Head of', '(Senior)']
    suffixes = ['(m/w/d)', '(w/m/d)', '(m/w)', '(w/m)', '(m/f/d)', '(f/m/d)', '(w/d/m)', '(d/w/m)', '(B.A.)',
                'am Campus oder virtuell', '(all genders)', '(d/f/m)', '(m/f/x)']

    for prefix in prefixes:
        if title.startswith(prefix):
            title = title[len(prefix):].strip()

    for suffix in suffixes:
        title = title.replace(suffix, '').strip()

    main_title = title.split(' - ')[0]  # Behandlung von Fällen mit' - '
    main_title = main_title.split(' / ')[0]  # Behandlung von Fällen mit' / '
    main_title = main_title.split(',')[0]  # Behandlung von Fällen mit ','

    return main_title

# Anwenden der Funktion auf die Spalte 'title'
data['simplified_title_v5'] = data['title'].apply(simplify_title_v5)

# Gruppierung ähnlicher Titel und Sicherstellung der Kombination von "Consultant" und "Berater" mit spezifischen Bereichen
def group_similar_titles_v2(title):
    title_map = {
        "Data Engineer": "Data Engineer",
        "Data Scientist": "Data Scientist",
        "Data Analyst": "Data Analyst",
        "Machine Learning Engineer": "Machine Learning Engineer",
        "Software Engineer": "Software Engineer",
        "DevOps Engineer": "DevOps Engineer",
        "Business Analyst": "Business Analyst",
        "Solution Architect": "Solution Architect",
        "IT-Architekt": "IT-Architekt",
        "SAP Consultant": ["SAP Consultant", "SAP Berater"],
        "Project Manager": ["Project Manager", "Projektleiter"],
        "Product Manager": ["Product Manager", "Produktmanager"],
        "Account Manager": ["Account Manager", "Kundenbetreuer"],
        "HR Manager": ["HR Manager", "Personalreferent"],
        "Marketing Manager": ["Marketing Manager", "Marketing Specialist"],
        "Finance Manager": ["Finance Manager", "Finanzmanager"],
        "Operations Manager": ["Operations Manager", "Betriebsleiter"],
        "Sales Manager": ["Sales Manager", "Vertriebsleiter"],
        "Full Stack Developer": ["Full Stack Developer", "Full-Stack-Entwickler"],
        "Frontend Developer": ["Frontend Developer", "Frontend-Entwickler"],
        "Backend Developer": ["Backend Developer", "Backend-Entwickler"],
        "System Administrator": ["System Administrator", "Systemadministrator"],
        "Network Engineer": ["Network Engineer", "Netzwerktechniker"],
        "Database Administrator": ["Database Administrator", "Datenbankadministrator"],
        "Security Analyst": ["Security Analyst", "Sicherheitsanalyst"],
        "Cloud Engineer": ["Cloud Engineer", "Cloud-Engineer"],
        "Data Architect": ["Data Architect", "Datenarchitekt"],
        "IT Consultant": ["IT Consultant", "IT-Berater"],
        "UX Designer": ["UX Designer", "UX-Designer"],
        "UI Designer": ["UI Designer", "UI-Designer"],
        "Scrum Master": "Scrum Master",
        "Agile Coach": "Agile Coach",
        "IT Support Specialist": ["IT Support Specialist", "IT-Support-Spezialist"],
        "Technical Writer": ["Technical Writer", "Technischer Redakteur"],
        "Quality Assurance Engineer": ["Quality Assurance Engineer", "Qualitätssicherungsingenieur"]
    }

    for key, variants in title_map.items():
        if isinstance(variants, list):
            for variant in variants:
                if variant.lower() in title.lower():
                    return key
        else:
            if key.lower() in title.lower():
                return key

    if "Consultant" in title or "Berater" in title:
        if len(title.split()) > 1:
            return title

    return title

# Anwenden der Gruppierungsfunktion auf die vereinfachten Titel
data['grouped_title_v2'] = data['simplified_title_v5'].apply(group_similar_titles_v2)

# Herausfiltern von Titeln, die nur "Consultant" oder "Berater" sind
data = data[~data['grouped_title_v2'].isin(['Consultant', 'Berater'])]

# Zählen der Vorkommen jedes gruppierten Jobtitels
grouped_title_counts_v2 = data['grouped_title_v2'].value_counts()

# Speichern der gezählten gruppierten Titel in einer CSV-Datei
output_file_path = '../Tables/grouped_job_titles_with_counts.csv'
grouped_title_counts_v2.to_csv(output_file_path, header=['Count'])

print(f"\nDie gruppierten Jobtitel wurden erfolgreich in '{output_file_path}' gespeichert.")

# Erhalten der Top 15 gruppierten Jobtitel für das Diagramm
top_15_grouped_titles_v2 = grouped_title_counts_v2.head(15)

# Erstellen eines Balkendiagramms für die Top 15 Jobtitel
plt.figure(figsize=(12, 8))
colors = plt.cm.tab20(np.linspace(0, 1, len(top_15_grouped_titles_v2)))
top_15_grouped_titles_v2.plot(kind='bar', color=colors)
plt.title('Top 15 KI-Stellenbezeichnungen', fontsize=15)
plt.xlabel('KI-Stellenbezeichnung', fontsize=12)
plt.ylabel('Anzahl', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Hinzufügen der Anzahl der Jobangebote als Beschriftung auf den Balken
for i in range(len(top_15_grouped_titles_v2)):
    plt.text(i, top_15_grouped_titles_v2[i] + 10, str(top_15_grouped_titles_v2[i]), ha='center', va='bottom')

# Anpassung der Ränder, um Platz für Beschriftungen zu schaffen
plt.subplots_adjust(bottom=0.25, left=0.15)
plt.show()
