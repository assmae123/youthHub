import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF

# --- Config page ---
st.set_page_config(page_title="YouthHub - Student Manager", layout="centered")

st.title("YouthHub - Gestion des Étudiants")
st.markdown("Gérez, analysez et exportez les notes des étudiants facilement avec YouthHub !")

# --- Style ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb, #90caf9);
    }
    div[data-testid="stToolbar"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# --- Charger ou créer CSV ---
try:
    df = pd.read_csv("students.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["id", "name", "grades"])

# --- Ajouter un étudiant ---
st.header("➕ Ajouter un étudiant")
name = st.text_input("Nom de l'étudiant")
if st.button("Ajouter"):
    if name:
        new_id = len(df) + 1
        df = pd.concat([df, pd.DataFrame({"id": [new_id], "name": [name], "grades": [""]})], ignore_index=True)
        df.to_csv("students.csv", index=False)
        st.success(f"Étudiant ajouté : {name}")
    else:
        st.warning("Entrez un nom valide.")

# --- Ajouter une note ---
st.header("📝 Ajouter une note")
student_id = st.number_input("ID de l'étudiant", min_value=1, step=1)
grade = st.number_input("Note", min_value=0.0, max_value=20.0, step=0.5)
if st.button("Enregistrer la note"):
    if student_id in df["id"].astype(int).values:
        i = df.index[df["id"].astype(int) == student_id][0]
        grades = df.at[i, "grades"]

        if pd.isna(grades) or str(grades).strip() == "":
            df.at[i, "grades"] = str(grade)

        else:
            df.at[i, "grades"] = str(grades) + ";" + str(grade)

        df.to_csv("students.csv", index=False)
        st.success("Note enregistrée !")
    else:
        st.error("ID non trouvé.")

# --- Supprimer un étudiant ---
st.header("🗑️ Supprimer un étudiant")
delete_id = st.number_input("ID à supprimer", min_value=1, step=1)
if st.button("Supprimer"):
    if delete_id in df["id"].astype(int).values:
        df = df[df["id"].astype(int) != delete_id]
        df.to_csv("students.csv", index=False)
        st.success(f"Étudiant {delete_id} supprimé.")
    else:
        st.warning("ID introuvable.")

# --- Modifier le nom ---
st.header("✏️ Modifier le nom d’un étudiant")
edit_id = st.number_input("ID de l'étudiant à modifier", min_value=1, step=1)
new_name = st.text_input("Nouveau nom")
if st.button("Modifier"):
    if edit_id in df["id"].astype(int).values:
        df.loc[df["id"].astype(int) == edit_id, "name"] = new_name
        df.to_csv("students.csv", index=False)
        st.success("Nom modifié avec succès !")
    else:
        st.warning("ID introuvable.")

# --- Calcul des moyennes safely ---
def safe_avg(grades):
    try:
        nums = [float(g.replace(',', '.')) for g in str(grades).split(';') if g.replace(',', '.').replace('.', '', 1).isdigit()]
        return sum(nums)/len(nums) if nums else 0
    except:
        return 0

if not df.empty:
    df["avg"] = df["grades"].apply(safe_avg)
    df = df.sort_values(by="avg", ascending=False)

# --- Afficher les étudiants ---
st.header("📋 Liste des étudiants")
if not df.empty:
    st.dataframe(df[["id", "name", "grades", "avg"]])
    st.markdown(f"**Moyenne générale : {df['avg'].mean():.2f}**")

# --- Graphique ---
st.header("📊 Moyenne des notes par étudiant")
if not df.empty:
    fig, ax = plt.subplots()
    sns.barplot(x="name", y="avg", data=df, palette="cool", dodge=False)
    ax.set_title("Moyenne par étudiant")
    st.pyplot(fig)

# --- Générer PDF sans emojis ---
def generate_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "YouthHub - Rapport des étudiants", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    for _, row in df.iterrows():
        pdf.cell(0, 10, f"{row['name']} : {row['avg']:.2f}", ln=True)

    pdf.ln(10)
    pdf.cell(0, 10, f"Moyenne générale : {df['avg'].mean():.2f}", ln=True)
    pdf.output("report_streamlit.pdf")

if st.button("Exporter en PDF"):
    generate_pdf(df)
    st.success("Rapport PDF généré avec succès : report_streamlit.pdf")

# --- Sauvegarder ---
if st.button("💾 Sauvegarder"):
    df.to_csv("students.csv", index=False)
    st.success("Données sauvegardées avec succès !")
