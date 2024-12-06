import os
import math
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def api_call(list_korrastatud):
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
                "content": f"{list_korrastatud}",
            }
        ]
    )
    response_content = chat_completion.choices[0].message.content

    return response_content


fail = "kontovv.csv"

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

esimene_pool = math.ceil(len(mainlist)/2)

elist = []
for i in range(0,esimene_pool):
    elist += [mainlist[i]]
tlist = []
for i in range(esimene_pool,len(mainlist)):
    tlist += [mainlist[i]]

print(api_call(elist))

print(api_call(tlist))