################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema:
# OpenAI abiga töötav finantside jälgija
#
# Autorid:
# Rainer Talvar, Mirko Sirila
#
# mõningane eeskuju:
# Probeeleme on lahendada aidanud Github Copilot, API requesti kood on kopeeritud OpenAI oma dokumentatsioonist
#
# Lisakommentaar (nt käivitusjuhend):
# Juhend on readme.md failis
##################################################

import os
from openai import OpenAI
from dotenv import load_dotenv
import tkinter
from tkinter import Tk, PhotoImage, filedialog
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()

#Raineri poolt REVOLUT csv faili korrastamine
def korista_list_REVOLUT(fail):
    suur_list = []

    with open(fail, "r", encoding="utf-8") as f:
            for rida in f:
                rida = rida.strip().split(",")
                suur_list.append(rida)

    korrastatud_list = []
    kasutu_info_indexid = [1, 3, 8, 9]

    for rida in suur_list:
        if (rida[0] == "CARD_PAYMENT" or rida[0] == "TOPUP" or rida[0] == "EXCHANGE") and rida[8] == "COMPLETED":
            korrastatud_list.append(rida)

    mainlist = []

    for rida in korrastatud_list:
        for i in sorted(kasutu_info_indexid, reverse=True):
            if i < len(rida):
                rida.pop(i)
        mainlist.append(rida)
        
    return mainlist

#Mirko poolt SEB csv faili korrastamine
def korista_list_SEB(fail):
    with open(fail, 'r', encoding='utf8') as f:
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

        return mainlist

#Raineri poolt kirjutatud API request, kui tegu on REVOLUT csv failiga
def api_call_REVOLUT(pool_korrastatud_list):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are an AI assistant specialized in processing financial transaction data. Your task is to analyze a Python double list of financial transactions and categorize each transaction accurately based on the provided merchant to assign it a label.

                Input: A list of transactions where each transaction is represented as a list:

                transactions = [['CARD_PAYMENT', '2024-09-30 14:03:38', 'Bolt', '-0.36', '0.00', 'EUR'], ['CARD_PAYMENT', '2024-09-30 14:06:41', 'Selver', '-3.49', '0.00', 'EUR'], ['CARD_PAYMENT', '2024-09-30 09:52:42', 'Selver', '-2.51', '0.00', 'EUR']]

                Categorization Guidelines:

                Toidukaubad: Konsum, Coop, Selver, Selver ABC, Maksimarket, Prisma, Carrefour, Rkiosk, Lidl, or similar.
                Transport: Bolt, Terravision, ATM - azienda trasporti milanesi, or other transport-related merchants.
                Ostlemine: Eeden, Klick, Ülemiste, Lõunakeskus, clothing stores like 24forever, h&m, nike, businesses such as OÜ, AS or similar.
                Kütus: CircleK, Neste, Terminal, Alexela, or similar.
                Baarid: Möku, Labor Baar, Club Studio, D3, Mits, or other bars and clubs.
                Väljas söömine: Restoran, Restaurant, Kohvik, Pizzakiosk, Mcdonalds, Hesburger, Chopsticks, Aparaat, Kolm Tilli, Ristogest, Picu Darbnīca or similar.
                Parkimine: parkla, parking, parkimine, Europark or related to parking.
                Reisimine: Lufthansa, Ryanair, Autodromo Nazionale Monza, airports (e.g., lennujaam or airport) or related to travelling.
                Sissetulekud: Apple pay top-up
                Valuuta vahetus: Exchange to USD or other currencies
                Microtransactions: Steam, Google payment, Twitch, or other online transactions.

                Output Requirements:

                Format: CSV
                Columns: Kategooria, Kuupäev, Firma, Summa, Valuuta
                Sort list Alphabetically based on label.
                Completeness: Ensure every original transaction is included in the final CSV.
                
                Be case-insensitive when matching merchant names.
                Assign the most specific category based on the order listed above.

                Output only the csv list and nothing else
                """
                    
            },
            {
                "role": "user",
                "content": f"{pool_korrastatud_list}",
            }
        ]
    )
    response_content = chat_completion.choices[0].message.content

    return response_content

#Mirko poolt kirjutatud API request, kui tegu on SEB csv failiga
def api_call_SEB(pool_korrastatud_list):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                No explanations, only answers I ask for.
                 
                Categorize ALL payments, make sure similar payments are in same category: 
                    Toidukaubad (toidukeskus, lihapood, lidl, konsum, coop, selver, maksimarket, maxima or any other grocery stores);
                    Tankla (circleK, neste, terminal, alexela and others);
                    Väljas söömine (restoran, kohvik, pizzakiosk, mcdonalds, HERBURGER, chopsticks, aparaat, kolm tilli or other);
                    Kõik internetiostud (websites, steam, gamerpay, google payment, online shopping (aliexpress, temu));
                    Parkimine (parkla, europark, snabb);
                    Transport (bolt, takso)
                    Ostlemine (clothing stores like 24forever, h&m, nike sportsdirect, sportland, rademar, businesses for example OÜ, AS, malls like ülemiste, lõunakeskus);
                    Riik/Pank (local banks such as SEB, SWED, Luminor, RAHANDUSMINISTEERIUM, ATM);
                    Muud (apteek, sent to/recieved from other people, autokool, haridus ja kultuuriselts, doesn't categorize exactly to others)

                Make a CSV compatible list where you separate categories and have payments in this form: nimi(not category),summa,kuupäev.
                """
            },
            {
                "role": "user",
                "content": f"{pool_korrastatud_list}",
            }
        ]
    )
    response_content = chat_completion.choices[0].message.content

    return response_content

def jaga_topeltlist_kaheks(korrastatud_list):
    keskkoht = len(korrastatud_list) // 2

    esimene_pool = korrastatud_list[:keskkoht]
    teine_pool = korrastatud_list[keskkoht:]

    return esimene_pool, teine_pool

def kirjuta_tagasi(fail, api_response_esimene, api_response_teine):

    korrastatud_esimene = api_response_esimene.replace('csv', '').replace('```', '').strip()
    korrastatud_teine = api_response_teine.replace('csv', '').replace('```', '').replace("Kategooria,Kuupäev,Firma,Summa,Valuuta", '').strip()

    with open(fail, "w", encoding="utf-8") as f:
        print(korrastatud_esimene + "\n" + korrastatud_teine, file=f)

    return fail

def visualiseeri_revolut(sisend_fail):
    fail = sisend_fail

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

def faili_asukoht(fail):
    failitee = os.path.join(fail)
    return failitee

def avafail():
    return filedialog.askopenfilename(title="Vali CSV fail", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

def run_tkinter():
    class PageSwitcherApp(Tk):
        def __init__(self) -> None:
            super().__init__()
            self.title("Finantside Jälgija")
            self.configure(background="black")
            self.eval('tk::PlaceWindow . center')
            self.minsize(600, 300)
            self.resizable(False, False)

            # Create a container for all pages
            container = tkinter.Frame(self)
            container.pack(fill="both", expand=True)

            # Dictionary to hold the pages
            self.frames = {}

            # Add pages to the dictionary
            for Leht in (Algus_leht, Loading_leht, Lopp_leht):
                page_name = Leht.__name__
                frame = Leht(parent=container, controller=self)
                self.frames[page_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")  # Stack all pages

            # Show the first page
            self.show_page("Algus_leht")

        def show_page(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    class Algus_leht(tkinter.Frame):
        def __init__(self, parent, controller) -> None:
            super().__init__(parent)
            self.controller = controller

            # Canvas setup for Page 1
            canvas = tkinter.Canvas(self, width=600, height=300, highlightthickness=0)
            canvas.pack(fill="both", expand=True)

            # Background image
            self.taust = PhotoImage(file="dimtaust.png")
            canvas.create_image(0, 0, anchor="nw", image=self.taust)

            # Instructions text
            canvas.create_text(300, 100, text="Sisesta oma panga (SEB, Revolut) kontoväljavõtte fail", font=("Helvetica", 12, "bold"), fill="white", anchor="center")

            # Button on canvas
            button_x1, button_y1 = 250, 150  # Top-left corner
            button_x2, button_y2 = 350, 180  # Bottom-right corner
            button = canvas.create_rectangle(button_x1, button_y1, button_x2, button_y2, fill="cyan", outline="white")

            # Button text
            canvas.create_text((button_x1 + button_x2) / 2, (button_y1 + button_y2) / 2, text="Ava fail", font=("Helvetica", 14), fill="black")

            # Function to handle button click
            def on_button_click(event):
                controller.show_page("Loading_leht")
                fail = faili_asukoht(avafail())
                main(fail)
                controller.show_page("Lopp_leht")

            # Bind the button to click event
            canvas.tag_bind(button, "<Button-1>", on_button_click)

    class Loading_leht(tkinter.Frame):
        def __init__(self, parent, controller):
            super().__init__(parent)
            self.controller = controller

            canvas = tkinter.Canvas(self, width=600, height=350, highlightthickness=0)
            canvas.pack(fill="both", expand=True)

            self.taust = PhotoImage(file="dimtaust.png")
            canvas.create_image(0, 0, anchor="nw", image=self.taust)

            # Loading text
            canvas.create_text(300, 150, text="Andmete töötlemine...", font=("Helvetica", 18, "bold"), fill="white", anchor="center")

    class Lopp_leht(tkinter.Frame):
        def __init__(self, parent, controller) -> None:
            super().__init__(parent)
            self.controller = controller

            canvas = tkinter.Canvas(self, width=600, height=350, highlightthickness=0)
            canvas.pack(fill="both", expand=True)

            self.taust = PhotoImage(file="dimtaust.png")
            canvas.create_image(0, 0, anchor="nw", image=self.taust)

            canvas.create_text(300, 150, text="Tulemused leiad failist final.xlsx", font=("Helvetica", 18, "bold"), fill="white", anchor="center")
            # Exit button
            button_x1, button_y1 = 250, 200  # Top-left corner
            button_x2, button_y2 = 350, 230  # Bottom-right corner
            button = canvas.create_rectangle(button_x1, button_y1, button_x2, button_y2, fill="cyan", outline="white")
            canvas.create_text((button_x1 + button_x2) / 2, (button_y1 + button_y2) / 2, text="Lõpeta", font=("Helvetica", 14), fill="black")
            canvas.tag_bind(button, "<Button-1>", lambda event: controller.destroy())

    app = PageSwitcherApp()
    app.mainloop()

def main(fail):
    fail1 = f"'{fail}'"

    if "csv" in fail1:
        if "kontovv.csv" in fail1:
            seb_list = korista_list_SEB(fail)

            esimene_pool, teine_pool = jaga_topeltlist_kaheks(seb_list)

            api_response_esimene = api_call_SEB(esimene_pool)
            api_response_teine = api_call_SEB(teine_pool)

            kirjuta_tagasi("kirjuta.csv", api_response_esimene, api_response_teine)
            print("TEST")
        elif "revolut" in fail1.lower():
            revolut_list = korista_list_REVOLUT(fail)

            esimene_pool, teine_pool = jaga_topeltlist_kaheks(revolut_list)

            api_response_esimene = api_call_REVOLUT(esimene_pool)
            api_response_teine = api_call_REVOLUT(teine_pool)

            sisend_fail = kirjuta_tagasi("kirjuta.csv", api_response_esimene, api_response_teine)
            visualiseeri_revolut(sisend_fail)
    else:
        print("Sellist faili pole, proovi uuesti")

if __name__ == "__main__":
    run_tkinter()