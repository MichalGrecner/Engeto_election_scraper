# Engeto_election_scraper
Engeto final project - election scraper

Tento projekt slouží k extrahování volebních výsledků z voleb v roce 2017. 

**Instalace knihoven**

Použité knihovny jsou uloženy v requirements.txt. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně: 

$ pip3 --version				            # ověřím verzi manažeru
$ pip3 install -r requirements.txt 	# nainstalujeme knihovny

**Spuštění projektu**

Spuštění souboru election_scraper.py 

Soubor election_scraper.py je nutné spouštět s dvěma argumenty. 
1. argument - odkaz na volební výsledky v úrovni volebních celků. 
2. argument - název souboru .csv s vyexportovanými výsledky z dané oblasti. 


**Příklad spuštění programu**

Argument1 (oblast Praha) - 
"https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100"

Argument2 - 
"praha_vysledky.csv" 

Program tedy spustíme následovně - příklad běhu programu:

python3 election_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100" "praha_vysledky.csv"
Stahuji data z url:  https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100
Ukládám do souboru:  praha_vysledky.csv
ukončuji



**ukázka částečného .csv výstupu**

code,location,registered,envelopes,
500054,Praha 1,21 556,14 167,
500224,Praha 10,79 964,52 277,
547034,Praha 11,58 353,39 306,

