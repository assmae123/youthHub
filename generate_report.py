# generate_report.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# --- قراءة البيانات ---
df = pd.read_csv("students_analyzed.csv")

# --- إنشاء الرسم ---
plt.figure(figsize=(6, 4))
sns.barplot(x="name", y="avg", data=df, palette="pastel")
plt.title("📊 Moyenne des notes par étudiant")
plt.xlabel("Étudiant")
plt.ylabel("Moyenne")
plt.ylim(0, 20)
plt.tight_layout()
plt.savefig("chart.png")
plt.close()

# --- إحصائيات عامة ---
nb_students = len(df)
mean_all = round(df["avg"].mean(), 2)
best_student = df.loc[df["avg"].idxmax()]
worst_student = df.loc[df["avg"].idxmin()]

# --- التحليل التلقائي ---
analysis_text = f"""
🏆 {best_student['name']} a la meilleure moyenne avec {best_student['avg']:.2f}.<br/>
⚠️ {worst_student['name']} a la moyenne la plus basse avec {worst_student['avg']:.2f}.<br/>
📈 La moyenne générale des étudiants est {mean_all}.
"""

# --- التوصيات الذكية ---
if best_student['avg'] >= 15:
    suggestion = f"🌟 Excellent travail, {best_student['name']}! Continue comme ça!"
else:
    suggestion = f"👍 Bon travail, {best_student['name']}, mais tu peux encore progresser."

if worst_student['avg'] < 10:
    suggestion += f"<br/>💪 {worst_student['name']}, essaie de revoir tes cours pour améliorer ta moyenne."
else:
    suggestion += f"<br/>👏 {worst_student['name']} montre un bon effort."

# --- إعداد التقرير ---
doc = SimpleDocTemplate("report.pdf")
styles = getSampleStyleSheet()
content = []

# العنوان والشعار
content.append(Image("logo.png", width=100, height=100))
content.append(Spacer(1, 10))
content.append(Paragraph("🎓 YouthHub - Rapport des étudiants", styles["Title"]))
content.append(Spacer(1, 20))

# الملخص العام
summary = f"""
Nombre total d'étudiants : {nb_students}<br/>
Moyenne générale : {mean_all}
"""
content.append(Paragraph("📋 Statistiques Générales :", styles["Heading2"]))
content.append(Paragraph(summary, styles["Normal"]))
content.append(Spacer(1, 20))

# التحليل الذكي
content.append(Paragraph("💬 Analyse automatique :", styles["Heading2"]))
content.append(Paragraph(analysis_text, styles["Normal"]))
content.append(Spacer(1, 20))

# توصيات ذكية
content.append(Paragraph("💡 Suggestions :", styles["Heading2"]))
content.append(Paragraph(suggestion, styles["Normal"]))
content.append(Spacer(1, 20))

# جدول منسق بالألوان
content.append(Paragraph("📊 Tableau des moyennes :", styles["Heading2"]))

table_data = [["Nom", "Moyenne"]] + df[["name", "avg"]].values.tolist()
table = Table(table_data, colWidths=[200, 100])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
]))
content.append(table)
content.append(Spacer(1, 20))

# الرسم البياني
content.append(Image("chart.png", width=400, height=300))

# حفظ الملف
doc.build(content)
print("✅ Rapport stylé généré avec succès: report.pdf")
