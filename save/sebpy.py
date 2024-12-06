import csv
import os
from openai import OpenAI
from dotenv import load_dotenv

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

        #csv.writer(excel).writerows(mainlist)

def api_call(list_korrastatud):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Write system prompt here"
            },
            {
                "role": "user",
                "content": list_korrastatud,
            }
        ]
    )
    response_content = chat_completion.choices[0].message.content

    return response_content