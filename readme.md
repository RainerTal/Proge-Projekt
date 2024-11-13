# OpenAI abiga töötav finantside jälgija

Enne programmi kävitamist on vaja Pythoni teeke openai ja dotenv
```
pip install openai dotenv
```

Peale seda on vaja luua endale .env fail oma arvutisse ning sinna sisse panna OpenAI API võti kujul
```
OPENAI_API_KEY="siia_oma_võti"
```

Siis saab programmi käivitada ja tuleb sisestada oma panga väljavõte hetkel, kas SEB-st või Revolutist

Programm jagab vastavad kulud kategooriatesse ning hetkel kirjutab need tagasi 'kirjuta.csv' faili.

Edaspidi töötame nende andmete visualiseerimisega