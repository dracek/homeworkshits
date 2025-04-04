import os
import numpy as np
from collections import Counter

# Pevně daná abeceda
ZNAKY = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"

SOURCE_DIR = os.path.join("resources", "book")
MATRIX_DIR = os.path.join("resources", "bigram_matice.csv")


def vytvor_bigramovou_matici_ze_slozky(slozka):
    """Načte všechny soubory ze složky a vytvoří bigramovou frekvenční matici. Počítá s už vyčištěným textem."""

    velikost = len(ZNAKY)
    index = {ch: i for i, ch in enumerate(ZNAKY)}
    matice = np.zeros((velikost, velikost), dtype=int)

    # Projdeme všechny soubory ve složce
    for soubor in os.listdir(slozka):
        cesta = os.path.join(slozka, soubor)

        if os.path.isfile(cesta):
            with open(cesta, "r", encoding="utf-8") as f:
                text = f.read()

            # Spočítáme bigramy
            bigramy = [text[i:i + 2] for i in range(len(text) - 1)]
            bigram_frekvence = Counter(bigramy)

            # Naplníme matici četností
            for bigram, pocet in bigram_frekvence.items():
                if bigram[0] in ZNAKY and bigram[1] in ZNAKY:
                    i, j = index[bigram[0]], index[bigram[1]]
                    matice[i, j] += pocet

    return matice

def normalizuj_matici(matice):
    """Normalizuje matici:
    1. Přičte 1 pouze k prvkům, které jsou 0.
    2. Normalizuje matici tak, aby součet všech prvků byl 1.
    """
    # Přičteme 1 jen k nulovým prvkům
    matice[matice == 0] = 1

    # Normalizace - vydělíme součtem celé matice
    return matice / np.sum(matice)


def uloz_matici_do_souboru(matice, soubor):
    """Uloží bigramovou matici do CSV souboru"""
    np.savetxt(soubor, matice, delimiter=",", fmt="%d")


def nacti_matici_ze_souboru(soubor):
    """Načte bigramovou matici z CSV souboru"""
    return np.loadtxt(soubor, delimiter=",", dtype=int)


if __name__ == "__main__":
    print("Vytvářím matici...")

    # Vytvoření matice
    matice = vytvor_bigramovou_matici_ze_slozky(SOURCE_DIR)

    # Uložení do souboru
    uloz_matici_do_souboru(matice, MATRIX_DIR)

    # Načtení a ověření
    nactena_matice = nacti_matici_ze_souboru(MATRIX_DIR)

    print("")
    print("uložená matice:")
    print(nactena_matice)

    print("")
    print("Normalizovaná matice:")
    print(normalizuj_matici(nactena_matice))
