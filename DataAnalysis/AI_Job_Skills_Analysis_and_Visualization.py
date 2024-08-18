import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np

# Datei einlesen
file_path = '../Daten/cleaned_merged_final.csv'
data = pd.read_csv(file_path)

# Zusammenfassung von verwandten Skills in Kategorien
skill_categories = {
    'Sprachen': {
        'Englisch': ['English', 'Englisch'],
        'Deutsch': ['German', 'Deutsch', 'Deutschkenntnisse'],
        'Andere Sprachen': ['Foreign Language Skills', 'Fremdsprachenkenntnisse']
    },
    'Soft Skills': {
        'Kommunikation': ['Communication', 'Kommunikation'],
        'Teamarbeit': ['Teamwork', 'Teamarbeit'],
        'Problemlösung': ['Problem Solving', 'Problemlösung'],
        'Kritisches Denken': ['Critical Thinking', 'Kritisches Denken'],
        'Zeitmanagement': ['Time Management', 'Zeitmanagement'],
        'Stressmanagement': ['Stress Management', 'Stressmanagement'],
        'Selbstmotivation': ['Self-motivation', 'Selbstmotivation'],
        'Flexibilität': ['Flexibility', 'Flexibilität'],
        'Kreativität': ['Creativity', 'Kreativität'],
        'Anpassungsfähigkeit': ['Adaptability', 'Anpassungsfähigkeit'],
        'Neugierde': ['Curiosity', 'Neugierde'],
        'Verhandlungsfähigkeit': ['Negotiation Skills', 'Verhandlungsfähigkeit'],
        'Präsentationsfähigkeiten': ['Presentation Skills', 'Präsentationsfähigkeiten']
    },
    'Hard Skills': {
        'Projektmanagement': ['Project Management', 'Projektmanagement'],
        'Finanzanalyse': ['Financial Analysis', 'Finanzanalyse'],
        'Datenanalyse': ['Data Analysis', 'Datenanalyse'],
        'IT-Kompetenzen': ['IT Skills', 'IT-Kompetenzen'],
        'Programmierung': ['Programming', 'Programmierung'],
        'Qualitätskontrolle': ['Quality Control', 'Qualitätskontrolle'],
        'Kundendienst': ['Customer Service', 'Kundendienst'],
        'Geschäftsanalyse': ['Business Analysis', 'Geschäftsanalyse'],
        'Computer Vision': ['Computer Vision', 'Computersicht'],
        'Deep Learning': ['Deep Learning', 'Tiefes Lernen'],
        'Cloud Computing': ['Cloud Computing', 'Cloud-Computing'],
        'Maschinelles Lernen': ['Machine Learning', 'Maschinelles Lernen'],
        'Statistische Analyse': ['Statistical Analysis', 'Statistische Analyse'],
        'Datenmodellierung': ['Data Modeling', 'Datenmodellierung'],
        'Datenbereinigung': ['Data Cleaning', 'Datenbereinigung'],
        'Automatisierung': ['Automation', 'Automatisierung'],
        'Weiterbildung': ['Continuing Education', 'Weiterbildung']
    }
}

# Zählen der Vorkommen jeder Fähigkeit
skill_counts = []
unique_descriptions = pd.Series(False, index=data.index)

# Zählen der Skills in allen Kategorien
for category, skills in skill_categories.items():
    for skill_group, terms in skills.items():
        # Escape special characters in terms for regex
        escaped_terms = [re.escape(term) for term in terms]
        # Kombinierte Bedingung für die Gruppe erstellen
        combined_condition = data['description'].str.contains(fr'(?i)\b(?:{"|".join(escaped_terms)})\b', regex=True)
        # Anzahl der Vorkommen der gesamten Gruppe
        count = combined_condition.sum()
        skill_counts.append([skill_group, count, category])
        # Aktualisiere die Gesamtheit der Beschreibungen, die mindestens eine Qualifikation enthalten
        unique_descriptions = unique_descriptions | combined_condition

# Erstellen eines DataFrames aus den Ergebnissen und Sortieren nach Vorkommen
skill_counts_df = pd.DataFrame(skill_counts, columns=['Skill', 'Anzahl', 'Kategorie']).sort_values(by='Anzahl', ascending=False)

# Ergebnisse ausgeben
print("\nVorkommen aller Fähigkeiten in den Jobbeschreibungen:")
print(skill_counts_df)

# Top 20 Skills anzeigen
top_20_skills = skill_counts_df.head(20)

# Ergebnisse ausgeben
print("\nTop 20 Fähigkeiten in den Jobbeschreibungen:")
print(top_20_skills)

unique_count_all = unique_descriptions.sum()
print(f"\nGesamtanzahl der Beschreibungen, die mindestens einen der Skills enthalten: {unique_count_all}")

# Funktion zum Erstellen eines Balkendiagramms
def create_bar_chart(data, title, x_label, y_label, x_ticks_rotation=0):
    plt.figure(figsize=(15, 10))

    # Farben aus der tab20 Palette zuweisen
    tab20_colors = plt.cm.tab20(np.linspace(0, 1, 20))
    category_colors = {
        'Sprachen': tab20_colors[0],
        'Soft Skills': tab20_colors[12],
        'Hard Skills': tab20_colors[8]
    }

    # Farben für die Balken basierend auf der Kategorie
    colors = []
    for skill in data['Skill']:
        for category, skills in skill_categories.items():
            if skill in skills:
                colors.append(category_colors[category])
                break

    bars = plt.bar(data['Skill'], data['Anzahl'], color=colors)
    plt.title(title, fontsize=14)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.xticks(ticks=np.arange(len(data['Skill'])), labels=data['Skill'], rotation=x_ticks_rotation, fontsize=10, ha='right')
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7)

    # Legende hinzufügen
    handles = [plt.Line2D([0], [0], color=color, lw=4) for color in category_colors.values()]
    labels = category_colors.keys()
    plt.legend(handles, labels, title='Kategorien', title_fontsize='13', fontsize='11')

    # Werte oben auf die Balken schreiben
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, int(yval), ha='center', fontsize=10)

    plt.tight_layout()
    plt.show()

# Balkendiagramm für die Top 20 Skills
create_bar_chart(top_20_skills, 'Top 20 Skills in den Jobbeschreibungen', 'Fähigkeit', 'Anzahl', 45)
