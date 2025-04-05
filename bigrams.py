import os
import numpy as np

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"

SOURCE_DIR = os.path.join("resources", "book")
MATRIX_PATH = os.path.join("resources", "bigram_matice.csv")

def get_bigrams(text):
    """Vytvoří seznam bigramů z textu."""
    bigrams_list = []
    n = len(text)

    for i in range(n - 1):
        bigram = text[i:i + 2]
        bigrams_list.append(bigram)

    return bigrams_list


def transition_matrix(bigrams):
    """Vytvoří bigramovou matici přechodů pro danou abecedu, nulové výskyty nahradí jedničkou"""
    global alphabet
    n = len(alphabet)

    # Inicializace matice n x n s nulami
    TM = np.zeros((n, n), dtype=int)

    # Mapování znaků na indexy
    char_to_index = {char: i for i, char in enumerate(alphabet)}

    # Naplnění matice četnostmi bigramů
    for bigram in bigrams:
        c1, c2 = bigram
        if c1 in char_to_index and c2 in char_to_index:
            i, j = char_to_index[c1], char_to_index[c2]
            TM[i, j] += 1
        else:
            raise Exception(f"Invalid bigram '{bigram}'")

    # Nahrazení nul hodnotou 1
    #TM[TM == 0] = 1

    return TM


def create_matrix_from_folder(slozka):
    """Načte texty, vytvoří bigramy a uloží bigramovou matici."""
    all_bigrams = []

    for filename in os.listdir(slozka):
        file_path = os.path.join(slozka, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        bigrams = get_bigrams(text)
        all_bigrams.extend(bigrams)

    return transition_matrix(all_bigrams)


def normalize_matrix(matice):
    """Normalizuje matici"""
    # Normalizace - vydělíme součtem celé matice
    return matice / np.sum(matice)


def save_matrix(matice, soubor):
    """Uloží bigramovou matici do CSV souboru"""
    np.savetxt(soubor, matice, delimiter=",", fmt="%d")


def load_matrix(soubor):
    """Načte bigramovou matici z CSV souboru"""
    return np.loadtxt(soubor, delimiter=",", dtype=int)

if __name__ == "__main__":
    print("Vytvářím matici...")

    # Vytvoření matice
    matice = create_matrix_from_folder(SOURCE_DIR)

    # Uložení do souboru
    save_matrix(matice, MATRIX_PATH)

    # Načtení a ověření
    nactena_matice = load_matrix(MATRIX_PATH)

    print("")
    print("uložená matice:")
    print(nactena_matice)

    print("")
    print("Normalizovaná matice:")
    print(normalize_matrix(nactena_matice))
