# visualize_students.py
import pandas as pd
import matplotlib.pyplot as plt

# Lecture du fichier analysé
df = pd.read_csv("students_analyzed.csv")

# Préparation du graphique
plt.figure(figsize=(6, 4))
plt.bar(df["name"], df["avg"], color="skyblue")
plt.title("Moyenne des notes par étudiant")
plt.xlabel("Étudiant")
plt.ylabel("Moyenne")
plt.ylim(0, 20)

# Affichage du graphique
plt.tight_layout()
plt.show()
