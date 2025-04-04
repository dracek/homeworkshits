import requests
from bs4 import BeautifulSoup
import roman
import os
import unicodedata
import re

# Konstanta pro poslední kapitolu
POSLEDNI_KAPITOLA = 54

CELKOVY_POCET_ZNAKU = 0

# Složka pro uložení souborů
OUTPUT_DIR = os.path.join("resources", "book")

# Zajistí, že složka existuje
os.makedirs(OUTPUT_DIR, exist_ok=True)


def stahni_text(roman_number):
    """Stáhne text z dané kapitoly"""
    url = f"https://cs.wikisource.org/wiki/Krakatit/{roman_number}."
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


def transformuj_text(text):
    """Transformuje text: odstraní diakritiku, nahradí nepísmenné znaky podtržítkem, odstraní duplicitní podtržítka a vrátí uppercase."""

    # Odstranění diakritiky
    text = ''.join(
        c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c)
    )

    text = re.sub(r'[^\w]', '_', text)  # Nahradí cokoliv, co není písmeno nebo číslo, podtržítkem
    text = re.sub(r'_+', '_', text)     # Odstraní opakující se podtržítka

    return text.upper()


def uloz_text(roman_number, text):
    """Uloží text do souboru v podsložce"""

    global CELKOVY_POCET_ZNAKU

    nazev_souboru = os.path.join(OUTPUT_DIR, f"Krakatit_{roman_number}.txt")

    with open(nazev_souboru, "w", encoding="utf-8") as file:
        file.write(text)

    CELKOVY_POCET_ZNAKU += len(text)

    print(f"Uloženo: {nazev_souboru}")


def uloz_text_main():
    # Stažení a zpracování všech kapitol
    for cislo in range(1, POSLEDNI_KAPITOLA + 1):
        roman_number = roman.toRoman(cislo)
        text = stahni_text(roman_number)

        if text:
            text = transformuj_text(text)
            uloz_text(roman_number, text)
    # Výpis celkového počtu znaků
    print(f"\nCelkový počet znaků ve všech kapitolách: {CELKOVY_POCET_ZNAKU}")



if __name__ == "__main__":
    print("Sosám text z wikisource...")
    uloz_text_main()

