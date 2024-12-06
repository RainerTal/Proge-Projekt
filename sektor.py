#pip install pandas
import pandas as pd
#pip install matplotlib
import matplotlib.pyplot as plt

df = pd.read_csv('kirjuta.csv')

df["summa"] = pd.to_numeric(df["summa"], errors="coerce")
kulud = df[df["summa"].notna()]

summad = kulud.groupby("category")["summa"].sum().reset_index()
print(summad)

labels = 'Toidukaubad', 'Tankla', 'Väljas söömine', 'Internetostud', 'Parkimine', 'Transport', 'Ostlemine', 'Riik/Pank', 'Muud'

plt.figure(figsize=(6,6))
plt.pie(summad["summa"], labels=summad['category'], autopct='%1.1f%%')
plt.title('Test')

pilt = 'chart.png'
plt.savefig(pilt, format='png')
plt.show()