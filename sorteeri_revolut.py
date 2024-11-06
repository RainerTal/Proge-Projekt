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

def main():
    suur_list = []

    with open("revolut_october.csv", "r", encoding="utf-8") as f:
        for rida in f:
            rida = rida.strip().split(",")
            suur_list.append(rida)
    
    print(korista_suur_list(suur_list))

if __name__ == "__main__":
    main()


