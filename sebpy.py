import csv

fail = 'kontovv.csv'

with open(fail, 'r', encoding='utf8') as f, open('andmed.csv', 'w', newline='') as excel:
        mainlist = []
        
        pealkirjad = ["Kuupäev", "Nimi/Esindus", "Summa", "Kirjeldus", "Teenustasu", "Valuuta"]
        mainlist.append(pealkirjad)
        
        f.readline()
        while True:
            rida = f.readline().strip()
            if rida == '':
                break
            rida = rida.split(';')
            valikud = [rida[2], rida[4], rida[8], rida[11], rida[12], rida[13]]
            valikud = [el.strip('"') for el in valikud]
            mainlist.append(valikud)

        csv.writer(excel).writerows(mainlist)