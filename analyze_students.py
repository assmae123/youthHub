# analyze_students.py
import pandas as pd

# Lecture des données
df = pd.read_csv("students.csv")

print("📂 Contenu du fichier :")
print(df)

# Conversion des colonnes
df["grades"] = df["grades"].apply(lambda x: [float(g) for g in str(x).split(";") if g])

# Création de nouvelles colonnes
df["avg"] = df["grades"].apply(lambda g: sum(g)/len(g) if g else 0)
df["count"] = df["grades"].apply(len)

print("\n📊 Statistiques générales :")
print("Nombre d'étudiants :", len(df))
print("Moyenne générale de tous les étudiants :", round(df["avg"].mean(), 2))

# Classement des étudiants par moyenne
print("\n🏆 Classement par moyenne :")
print(df[["name", "avg"]].sort_values("avg", ascending=False))

# Sauvegarde des résultats dans un nouveau fichier
df.to_csv("students_analyzed.csv", index=False)
print("\n💾 Les résultats ont été enregistrés dans students_analyzed.csv")
