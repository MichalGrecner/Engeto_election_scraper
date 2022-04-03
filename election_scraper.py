import requests
from bs4 import BeautifulSoup
import csv
import sys


def main():
    odkaz_uz_cel = sys.argv[1]
    file_name = sys.argv[2]
    soup_uz_cel = uz_cel_odpoved_serveru(odkaz_uz_cel)
    odkazy = list_odkazu_obci(soup_uz_cel)
    soup_obec = obec_odpoved_serveru(odkazy[0])
    print("Stahuji data z url: ", odkaz_uz_cel)
    data = list_udaju_obci(soup_uz_cel, odkazy)
    header = header_tabulky(soup_obec)
    print("Ukládám do souboru: ", file_name)
    export_do_csv(header, data, file_name)


def list_udaju_obci(soup_uz_cel, odkazy):
    """
    Funkce vytváří list listů, kdy každý list jsou údaje ke každé obci a později tedy jeden řádek v csv tabulce
    """
    udaje_obci = []
    kody_obci = list_kodu_obci(soup_uz_cel)
    nazvy_obci = list_nazvu_obci(soup_uz_cel)
    for i, url in enumerate(odkazy):
        udaje = []
        udaje.append(kody_obci[i])
        udaje.append(nazvy_obci[i])
        udaje.append(volici_v_seznamu(obec_odpoved_serveru(url)))
        udaje.append(vydane_obalky(obec_odpoved_serveru(url)))
        udaje.append(platne_hlasy(obec_odpoved_serveru(url)))
        hlasy_strany = kandidujici_strany_hlasy(obec_odpoved_serveru(url))
        for hlasy in hlasy_strany.values():
            udaje.append(hlasy)
        udaje_obci.append(udaje)
    return udaje_obci


def obec_odpoved_serveru(url):
    odpoved_obec = requests.get(url)
    return BeautifulSoup(odpoved_obec.text, "html.parser")


def uz_cel_odpoved_serveru(url):
    odpoved_uz_cel = requests.get(url)
    return BeautifulSoup(odpoved_uz_cel.text, "html.parser")


def kod_obce(soup):
    kod1 = soup.find("td", {"class": "cislo"})
    kod2 = kod1.find("a")
    return kod2.get_text()


def volici_v_seznamu(soup):
    vypis = []
    for radek in soup.find_all("td", {"class": "cislo"}):
        vypis.append(radek.get_text(""))
    return vypis[3]


def vydane_obalky(soup):
    vypis = []
    for radek in soup.find_all("td", {"class": "cislo"}):
        vypis.append(radek.get_text(""))
    return vypis[4]


def platne_hlasy(soup):
    vypis = []
    for radek in soup.find_all("td", {"class": "cislo"}):
        vypis.append(radek.get_text(""))
    return vypis[7]


def kandidujici_strany(soup) -> list:
    vypis = []
    for radek in soup.find_all("td", {"class": "overflow_name"}):
        vypis.append(radek.get_text(""))
    return vypis


def kandidujici_strany_hlasy(soup) -> dict:
    """
    Fce zjišťuje kolik hlasů má jaká politická strana v dané obci
    """
    strany_hlasy = {}
    for tabulka in soup.find_all("div", {"id": "inner"}):
        for radek in tabulka.find_all("tr"):
            if radek.find("td", {"class": "overflow_name"}):
                nazev = radek.find("td", {"class": "overflow_name"})
                for i, cislo in enumerate(radek.find_all("td", {"class": "cislo"})):
                    if i == 1:
                        strany_hlasy[nazev.get_text()] = cislo.get_text()
    return strany_hlasy


def list_odkazu_obci(soup) -> list:
    """
    ze SOUPu volebního územního celku vrací list s odkazy na jednotlivé obce
    """
    odkazy_obci = []
    zacatek_odkazu = "https://volby.cz/pls/ps2017nss/"
    odkazy = soup.find("div", {"id": "inner"})
    for n, spinavy_odkaz in enumerate(odkazy.find_all("a")):
        if n % 2 == 0:
            konec_odkazu = str(spinavy_odkaz.get("href"))
            odkaz = zacatek_odkazu + konec_odkazu
            odkazy_obci.append(odkaz)
    return odkazy_obci


def list_kodu_obci(soup) -> list:
    kody_obci = []
    kody = soup.find("div", {"id": "inner"})
    for spinavy_kod in kody.find_all("td", {"class": "cislo"}):
        kod_tag = spinavy_kod.find("a")
        kody_obci.append(kod_tag.get_text())
    return kody_obci

def list_nazvu_obci(soup) -> list:
    nazvy_obci = []
    nazvy = soup.find("div", {"id": "inner"})
    for spinavy_nazev in nazvy.find_all("td",{"class":"overflow_name"}):
        nazvy_obci.append(spinavy_nazev.get_text())
    return nazvy_obci


def header_tabulky(soup):
    header = ["code", "location", "registered", "envelopes", "valid"]
    for strana in kandidujici_strany(soup):
        header.append(strana)
    return header


def export_do_csv(header, data, nazev):
    with open(nazev, "w", newline="", encoding="utf-8") as file:
        file_write = csv.writer(file)
        file_write.writerow(header)
        file_write.writerows(data)


if __name__ == "__main__":
    try:
        main()
    except:
        print("Nesprávně zadané argumenty")
    finally:
        print("ukončuji")
        quit()

