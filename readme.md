# OpenAI abiga töötav finantside jälgija

Enne programmi kävitamist on vaja Pythoni teeke openai, dotenv, pandas ja matplotlib
```
pip install -r req.txt
```

Peale seda on vaja luua endale .env fail oma arvutisse ning sinna sisse panna OpenAI API võti kujul
```
OPENAI_API_KEY="siia_oma_võti"
```

Siis saab programmi käivitada ja tuleb sisestada oma panga väljavõte hetkel, kas SEB-st või Revolutist

Programm jagab vastavad kulud kategooriatesse ning kirjutab need csv formaadis tagasi 'kirjuta.csv' faili

Siis võtab programm ette antud 'kirjuta.csv' faili ning OpenAI API päring jagab kulud kategooriatesse. Matplotlib ja Pandas teekidega visualiseerib programm andmed faili 'final.xlsx'
