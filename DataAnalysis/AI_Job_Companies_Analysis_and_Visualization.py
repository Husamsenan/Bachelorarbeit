import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Laden der Daten
file_path = '../Daten/cleaned_merged_final.csv'
data = pd.read_csv(file_path)

# Zählen der Vorkommen jedes Unternehmens in der Spalte company_name
company_counts = data['company_name'].value_counts()

# Speichern der Daten als CSV-Datei
output_file_path = '../Tables/company_job_counts.csv'  # Passe den Dateinamen nach Bedarf an
company_counts.to_csv(output_file_path, header=['Anzahl der Jobangebote'])

# Sicherstellen, dass die Top 100 Unternehmen vollständig angezeigt werden
pd.set_option('display.max_rows', 100)

# Ausgabe der Top 100 Unternehmen in der Konsole
top_100_companies = company_counts.head(100)
print("\nTop 100 Unternehmen nach Anzahl der Jobangebote:")
print(top_100_companies)

# Erhalten der Top 15 Unternehmen
top_15_companies = company_counts.head(15)

# Erstellen eines Balkendiagramms für die Top 15 Unternehmen
plt.figure(figsize=(12, 8))
colors = plt.cm.tab20(np.linspace(0, 1, len(top_15_companies)))
ax = top_15_companies.plot(kind='bar', color=colors)
plt.title('Top 15 Unternehmen nach Jobangeboten', fontsize=16)
plt.xlabel('Unternehmen', fontsize=14)
plt.ylabel('Anzahl der Jobangebote', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Hinzufügen der Anzahl der Jobangebote als Beschriftung auf den Balken
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height() + 5), ha='center', va='bottom')

# Diagramm anzeigen
plt.tight_layout()
plt.show()

# Rücksetzen der Anzeigeoptionen, falls erforderlich
pd.reset_option('display.max_rows')
