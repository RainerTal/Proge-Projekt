import csv
import os
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
                "content": """No explanations, only answers I ask for. I want you to add up all amounts and service fees. Now categorize them accordingly: 
                groceries (konsum, coop, selver, maksimarket or any other grocery stores);
                shopping (eeden; ülemiste; lõunakeskus; clothing stores like 24forever, h&m, nike, businesses for example OÜ, AS);
                fuel (circleK, neste, terminal, alexela and others);
                eating out (restoran, kohvik, pizzakiosk, mcdonalds, hesburger, chopsticks, aparaat, kolm tilli or other);
                microtransactions (steam, google payment);
                parking (parkla, parking, park, europark);
                other (sent to or by other people, you can  or unknown). Let me know which ones are unknown to you."""
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

        #csv.writer(excel).writerows(mainlist)

print(api_call(mainlist))