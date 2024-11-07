import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def korista_suur_list(suur_list):
    korrastatud_list = []
    kasutu_info_indexid = [1, 3, 8, 9]

    for rida in suur_list:
        if (rida[0] == "CARD_PAYMENT" or rida[0] == "TOPUP") and rida[8] == "COMPLETED":
            korrastatud_list.append(rida)

    loplik_list = []

    for rida in korrastatud_list:
        for i in sorted(kasutu_info_indexid, reverse=True):
            if i < len(rida):
                rida.pop(i)
        loplik_list.append(rida)
        
    return loplik_list

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


def main():
    suur_list = []

    with open("revolut_october.csv", "r", encoding="utf-8") as f:
        for rida in f:
            rida = rida.strip().split(",")
            suur_list.append(rida)
    
    korrastatud = (korista_suur_list(suur_list))

    api_res = api_call(korrastatud)
    print(api_res)

if __name__ == "__main__":
    main()


