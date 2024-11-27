import pandas as pd
import matplotlib.pyplot as plt

fail = 'andmed.csv'
output_fail = 'final.xlsx'

loe_andmed = pd.read_csv(fail)

loe_andmed['Kuupäev'] = pd.to_datetime(loe_andmed['Kuupäev'], errors='coerce')
loe_andmed['Summa'] = pd.to_numeric(loe_andmed['Summa'], errors='coerce')

sorteeritud_andmed = loe_andmed.sort_values(by=['Kategooria', 'Summa'], ascending=[True, True])

kulud = loe_andmed[loe_andmed['Summa'] < 0]
tulud = loe_andmed[loe_andmed['Summa'] > 0]

kulude_summad = kulud.groupby(['Kategooria', 'Valuuta'])['Summa'].sum().abs().reset_index()
kulude_summad = kulude_summad[['Kategooria', 'Summa', 'Valuuta']]

tulude_summad = tulud.groupby(['Kategooria', 'Valuuta'])['Summa'].sum().reset_index()
tulude_summad = tulude_summad[['Kategooria', 'Summa', 'Valuuta']]

plt.figure(figsize=(6, 7))
pie_chart_path = 'pie_chart.png'
plt.pie(kulude_summad['Summa'], labels=kulude_summad['Kategooria'], autopct='%1.1f%%', labeldistance=1.2, pctdistance=0.8)
plt.title('Kulude osakaal kategooriatena')
plt.savefig(pie_chart_path)  
plt.close()

kulud = kulud.sort_values('Kuupäev')  
kulud = kulud.dropna(subset=['Kuupäev'])  
kulud['Kokku kulutus'] = kulud['Summa'].cumsum().abs()

plt.figure(figsize=(8, 4))
trend_chart_path = 'trend_chart.png'
plt.plot(kulud['Kuupäev'], kulud['Kokku kulutus'], marker='o', linestyle='-', linewidth=2)
plt.title('Kulutuste trend', fontsize=10)
plt.xlabel('Kuupäev', fontsize=8)
plt.ylabel('Kulutused (€)', fontsize=8)
plt.grid(True)
plt.xticks(rotation=45)  
plt.savefig(trend_chart_path)  
plt.close()

with pd.ExcelWriter('final.xlsx', engine='xlsxwriter') as writer:
    sorteeritud_andmed.to_excel(writer, sheet_name="Kõik kulud ja tulud", index=False)
    kulude_summad.to_excel(writer, sheet_name="Kulude ja tulude summad", index=False)

    workbook = writer.book
    worksheet = writer.sheets["Kõik kulud ja tulud"]

    worksheet.insert_image('L2', pie_chart_path)  
    worksheet.insert_image('L22', trend_chart_path)  