import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np

# Datei einlesen
file_path = '../Daten/cleaned_merged_final.csv'
data = pd.read_csv(file_path)

# Liste von AI-Technologien und deren Kategorien
ai_technologies = {
    'Programmiersprachen': ['Python', 'R', 'Java', 'C++', 'C#', 'Go', 'Julia', 'Node.js', 'JavaScript'],
    'Bibliotheken/Frameworks': ['TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'Pandas', 'NumPy', 'Hugging Face Transformers', 'OpenCV', 'spaCy', 'NLTK', 'XGBoost', 'LightGBM', 'CatBoost', 'Caffe', 'MXNet', 'Spring Boot', 'Angular'],
    'Datenbanken': ['SQL', 'NoSQL', 'MySQL', 'PostgreSQL', 'Oracle', 'MariaDB', 'DynamoDB', 'Cassandra', 'MongoDB', 'Redis', 'Neo4j', 'Elasticsearch'],
    'Cloud-Plattformen': ['AWS', 'Azure', 'Google Cloud'],
    'Tools': ['Jupyter Notebooks', 'Streamlit', 'Git', 'GitHub Copilot', 'Docker', 'Kubernetes', 'Ansible', 'DevOps', 'MLOps', 'AutoML', 'Kubeflow', 'MLflow', 'DVC', 'Tableau', 'Power BI'],
    'Andere': ['Generative AI', 'DALL-E', 'OpenAI', 'ChatGPT']
}

# Escape special characters in technology names for regex
escaped_technologies = [re.escape(tech) for category in ai_technologies.values() for tech in category]

# Zählen der Vorkommen jeder Technologie unter Berücksichtigung von Wortgrenzen und Groß-/Kleinschreibung
technology_counts = {}
for category, tech_list in ai_technologies.items():
    for tech in tech_list:
        escaped_tech = re.escape(tech)
        count = data['description'].str.contains(fr'\b{escaped_tech}\b', case=False, regex=True).sum()
        technology_counts[tech] = (count, category)

# Erstellen eines DataFrames aus den Ergebnissen und Sortieren nach Vorkommen
technology_counts_df = pd.DataFrame.from_dict(technology_counts, orient='index', columns=['count', 'category']).sort_values(by='count', ascending=False)

# Anzeige aller Zeilen und Spalten in der Konsole
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Gesamte Liste der Technologien und deren Zählungen ausgeben
print("\nVorkommen aller AI-Technologien in den Jobbeschreibungen:")
print(technology_counts_df)

# Top 20 Technologien anzeigen
top_20_technologies = technology_counts_df.head(20)

# Ergebnisse ausgeben
print("\nTop 20 AI-Technologien in den Jobbeschreibungen:")
print(top_20_technologies)

# Funktion zum Erstellen eines Balkendiagramms
def create_bar_chart(data, title, x_label, y_label, x_ticks_rotation=0):
    plt.figure(figsize=(15, 10))

    # Farben aus der tab20 Palette zuweisen
    tab20_colors = plt.cm.tab20(np.linspace(0, 1, 20))
    category_colors = {
        'Programmiersprachen': tab20_colors[0],
        'Bibliotheken/Frameworks': tab20_colors[4],
        'Datenbanken': tab20_colors[8],
        'Cloud-Plattformen': tab20_colors[12],
        'Tools': tab20_colors[16],
        'Andere': tab20_colors[18]
    }

    colors = [category_colors[category] for category in data['category']]

    bars = plt.bar(data.index, data['count'], color=colors)
    plt.title(title, fontsize=14)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.xticks(rotation=x_ticks_rotation, fontsize=10)
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

# Balkendiagramm für die Top 20 AI-Technologien
create_bar_chart(top_20_technologies, 'Top 20 AI-Technologien in den Jobbeschreibungen', 'Technologie', 'Anzahl', 45)
