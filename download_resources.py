import requests
from bs4 import BeautifulSoup
import os
import unicodedata
import re

from config import DOWNLOAD_DIR


def download_text(url):
    """Stáhne text z daného wikisource zdroje"""
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Chyba při stahování {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    obsah_divu = soup.find("div", class_="forma proza")

    if obsah_divu:
        return obsah_divu.get_text(separator="\n", strip=True)
    else:
        print(f"Nenalezen požadovaný div na stránce {url}")
        return None


def transform_text(text):
    """Transformuje text: odstraní diakritiku, nahradí nepísmenné znaky podtržítkem, odstraní duplicitní podtržítka a vrátí uppercase."""

    # Odstranění diakritiky
    text = ''.join(
        c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c)
    )

    text = re.sub(r'[^A-Za-z]', '_', text)  # Nahradí vše kromě písmen podtržítkem
    text = re.sub(r'_+', '_', text)         # Odstraní opakující se podtržítka

    return text.upper()


def save_text(name, text):
    """Uloží text do souboru v podsložce"""

    nazev_souboru = os.path.join(DOWNLOAD_DIR, f"{name}.txt")

    with open(nazev_souboru, "w", encoding="utf-8") as file:
        file.write(text)

    print(f"Uloženo: {nazev_souboru}")


def extract_links_from_url(url, prefix=""):
    """Stáhne HTML ze zadané URL a extrahuje odkazy z <li> elementů uvnitř <div id='mw-content-text'>.
    Funguje pro <ol> i <ul>, ignoruje <ol> s class='references'. Mezery a tečky v textu odkazu jsou odstraněny."""

    base_url = "https://cs.wikisource.org"

    response = requests.get(base_url + url)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Najdeme hlavní obsahový div
    content_div = soup.find("div", id="mw-content-text")
    if not content_div:
        return []

    links = []

    # Projdeme všechny <ol> a <ul> uvnitř divu
    for lst in content_div.find_all(["ol", "ul"]):
        if lst.name == "ol" and "references" in lst.get("class", []):
            continue  # Přeskočíme tento seznam

        # Projdeme <li> uvnitř seznamu
        for li in lst.find_all("li"):
            a_tag = li.find("a", href=True)
            if a_tag:
                text = "".join(a_tag.stripped_strings).replace(" ", "_").replace(".", "")
                links.append((prefix + text, base_url + a_tag["href"]))

    return links


def main():

    url_list = []
    celkovy_pocet_znaku = 0

    url_list.extend(extract_links_from_url("/wiki/Krakatit", "Krakatit_"))
    url_list.extend(extract_links_from_url("/wiki/Jak_se_co_d%C4%9Bl%C3%A1"))

    # Zajistí, že cílová složka existuje
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Stažení a zpracování všech kapitol
    for name, url in url_list:
        text = download_text(url)

        if text:
            text = transform_text(text)
            save_text(name, text)

            celkovy_pocet_znaku += len(text)
        else:
            print(f"Problém se zdrojem {name}!")

    print(f"Nasosáno a uloženo {celkovy_pocet_znaku} znaků.")


if __name__ == "__main__":
    print("Sosám texty z wikisource...")
    main()


