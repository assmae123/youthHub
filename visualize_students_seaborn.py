# visualize_students_seaborn.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# قراءة البيانات
df = pd.read_csv("students_analyzed.csv")

# إعداد الشكل
plt.figure(figsize=(7, 5))
sns.barplot(x="name", y="avg", data=df, palette="pastel")

# إضافة العناوين
plt.title("📊 Moyenne des notes par étudiant", fontsize=14)
plt.xlabel("Étudiant", fontsize=12)
plt.ylabel("Moyenne", fontsize=12)
plt.ylim(0, 20)

# كتابة المعدل فوق كل عمود
for i, val in enumerate(df["avg"]):
    plt.text(i, val + 0.3, f"{val:.1f}", ha='center', fontsize=10, color='black')

plt.tight_layout()
plt.show()
