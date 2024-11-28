import pandas as pd
import matplotlib.pyplot as plt

fail = 'andmed.csv'
output_fail = 'final.xlsx'

loe_andmed = pd.read_csv(fail)

# Kuupäevad str -> kuupäev | Summad str -> num

loe_andmed['Kuupäev'] = pd.to_datetime(loe_andmed['Kuupäev'], errors='coerce')
loe_andmed['Summa'] = pd.to_numeric(loe_andmed['Summa'], errors='coerce')

sorteeritud_andmed = loe_andmed.sort_values(by=['Kategooria', 'Summa'], ascending=[True, True])

kulud = loe_andmed[loe_andmed['Summa'] < 0]
tulud = loe_andmed[loe_andmed['Summa'] > 0]

kulude_summad = kulud.groupby(['Kategooria', 'Valuuta'])['Summa'].sum().abs().reset_index()
kulude_summad = kulude_summad[['Kategooria', 'Summa', 'Valuuta']]

tulude_summad = tulud.groupby(['Kategooria', 'Valuuta'])['Summa'].sum().reset_index()
tulude_summad = tulude_summad[['Kategooria', 'Summa', 'Valuuta']]


# Vahelduvus suurte ja väikeste kulude kategooriate vahel, et pie chart oleks loetavam
kokku = kulude_summad['Summa'].sum()
vaiksed_threshold = kokku * 0.02

suured_kategooriad = kulude_summad[kulude_summad['Summa'] >= vaiksed_threshold]
vaiksed_kategooriad = kulude_summad[kulude_summad['Summa'] < vaiksed_threshold]

vahelduvus = []
suur_idx, vaike_idx = 0, 0
while suur_idx < len(suured_kategooriad) or vaike_idx < len(vaiksed_kategooriad):
    if suur_idx < len(suured_kategooriad):
        vahelduvus.append(suured_kategooriad.iloc[suur_idx])
        suur_idx += 1
    if vaike_idx < len(vaiksed_kategooriad):
        vahelduvus.append(vaiksed_kategooriad.iloc[vaike_idx])
        vaike_idx += 1
vahelduvus = pd.DataFrame(vahelduvus)

# Pie charti genereerimine

suurus = vahelduvus['Summa']
kategooria = vahelduvus['Kategooria']

plt.figure(figsize=(6, 6))
pie_chart_path = 'pie_chart.png'
plt.pie(suurus, labels=kategooria, autopct='%1.1f%%', labeldistance=1.02, pctdistance=0.8)
plt.title('Kulude osakaal kategooriatena')
plt.savefig(pie_chart_path)  
plt.close()

kulud = kulud.sort_values('Kuupäev')  
kulud = kulud.dropna(subset=['Kuupäev'])  
kulud['Kokku kulutus'] = kulud['Summa'].cumsum().abs()

# Trend charti genereerimine

plt.figure(figsize=(8, 6.5))
trend_chart_path = 'trend_chart.png'
plt.plot(kulud['Kuupäev'], kulud['Kokku kulutus'], marker='o', linestyle='-', linewidth=2)
plt.title('Kulutuste trend', fontsize=10)
plt.xlabel('Kuupäev', fontsize=7)
plt.ylabel('Kulutused (€)', fontsize=7)
plt.grid(True)
plt.xticks(rotation=45)  
plt.savefig(trend_chart_path)  
plt.close()

# Kõik exceli faili tagasi kirjutamine

with pd.ExcelWriter('final.xlsx', engine='xlsxwriter') as writer:
    sorteeritud_andmed.to_excel(writer, sheet_name="Kõik kulud ja tulud", index=False)
    kulude_summad.to_excel(writer, sheet_name="Kulude ja tulude summad", startcol=0, startrow=2, index=False)
    tulude_summad.to_excel(writer, sheet_name="Kulude ja tulude summad", startcol=5, startrow=2, index=False)

    workbook = writer.book
    worksheet = writer.sheets["Kõik kulud ja tulud"]
    worksheet2 = writer.sheets["Kulude ja tulude summad"]

    worksheet2.write(0, 1, "Kulude summa")
    worksheet2.write(1, 5, "Tulude summa")

    worksheet.insert_image('H2', pie_chart_path)  
    worksheet.insert_image('H35', trend_chart_path)  