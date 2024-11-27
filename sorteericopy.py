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
                Columns: label, date, merchant, amount, currency.
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
                No explanations, only answers.
                 
                Categorize ALL payments, make sure similar payments are in same category, amount must be float: 
                    Toidukaubad (toidukeskus, lihapood, lidl, konsum, coop, selver, maksimarket, maxima or any other grocery stores);
                    Tankla (circleK, neste, terminal, alexela and others);
                    Väljas söömine (restoran, kohvik, pizzakiosk, mcdonalds, HERBURGER, chopsticks, aparaat, kolm tilli or other);
                    Internet (websites, steam, gamerpay, google payment, online shopping (aliexpress, temu));
                    Parkimine (parkla, europark, snabb);
                    Transport (bolt, takso)
                    Ostlemine (clothing stores like 24forever, h&m, nike sportsdirect, sportland, rademar, businesses for example OÜ, AS, malls like ülemiste, lõunakeskus);
                    Riik/Pank (local banks such as SEB, SWED, Luminor, RAHANDUSMINISTEERIUM, ATM);
                    Muud (apteek, sent to/recieved from other people, autokool, haridus ja kultuuriselts, doesn't categorize exactly to others)
                Make a CSV compatible list with all lines where you separate categories in these columns: category,nimi,summa,kuupäev.
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

    api_response_esimene = api_response_esimene.replace('csv', '').replace('```', '').strip()
    api_response_teine = api_response_teine.replace('csv', '').replace('```', '').strip()

    with open(fail, "w", encoding="utf-8") as f:
        print(f"{api_response_esimene}", file=f)
        print(f"{api_response_teine}", file=f)

def main():
    fail = input("Sisesta .csv faili nimi, mille sees oleks soovitud panga nimi: ")

    while True:
        if os.path.isfile(fail) and "csv" in fail:
            if fail.lower() == "kontovv.csv":
                seb_list = korista_list_SEB(fail)

                esimene_pool, teine_pool = jaga_topeltlist_kaheks(seb_list)

                api_response_esimene = api_call_SEB(esimene_pool)
                api_response_teine = api_call_SEB(teine_pool)

                kirjuta_tagasi("kirjuta.csv", api_response_esimene, api_response_teine)
                break
            elif "revolut" in fail.lower():
                revolut_list = korista_list_REVOLUT(fail)

                esimene_pool, teine_pool = jaga_topeltlist_kaheks(revolut_list)

                api_response_esimene = api_call_REVOLUT(esimene_pool)
                api_response_teine = api_call_REVOLUT(teine_pool)

                kirjuta_tagasi("kirjuta.csv", api_response_esimene, api_response_teine)
                break
            else:
                break
        else:
            print("Sellist faili pole, proovi uuesti")
            fail = input("Sisesta .csv faili nimi, mille sees oleks soovitud panga nimi, ENTER, et lõpetada: ")
            if fail == "":
                break
            else:
                continue
    
if __name__ == "__main__":
    main()


