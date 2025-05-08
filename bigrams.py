import os
import numpy as np

from config import alphabet, DOWNLOAD_DIR, MATRIX_PATH


def get_bigrams(text):
    """
    Vytvoří seznam bigramů (dvojic po sobě jdoucích znaků) z daného textu.

    Args:
        text (str): Vstupní text, ze kterého se budou tvořit bigramy. Očekává se
                    neprázdný řetězec. Délka by měla být alespoň 2 znaky,
                    jinak bude výstup prázdný seznam.

    Returns:
        list[str]: Seznam řetězců, kde každý prvek představuje jeden bigram
                   získaný z po sobě jdoucích znaků vstupního textu.
    """
    bigrams_list = []
    n = len(text)

    for i in range(n - 1):
        bigram = text[i:i + 2]
        bigrams_list.append(bigram)

    return bigrams_list


def transition_matrix_raw(bigrams):
    """
    Vytvoří bigramovou matici přechodů pro danou abecedu, kde každý prvek matice udává počet výskytů
    příslušného bigramu. Zachovává nulové četnosti pro výpočet TM_obs.

    Args:
        bigrams (list[str]): Seznam bigramů (dvojic znaků).

    Returns:
        numpy.ndarray: Čtvercová matice velikosti n x n (kde n je délka abecedy), obsahující
                       četnosti přechodů mezi znaky. Nulové četnosti jsou zachovány."""

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
            raise ValueError(f"Invalid bigram '{bigram}'")

    return TM


def transition_matrix(bigrams):
    """
    Vytvoří bigramovou matici přechodů s použitím pomocné funkce transition_matrix_raw(bigrams).
    Nulové výskyty jsou nahrazeny jedničkou kvůli pozdějšímu logaritmování hodnot.

    Args:
        bigrams (list[str]): Seznam bigramů (dvojic znaků).

    Returns:
        numpy.ndarray: Čtvercová matice velikosti n x n (kde n je délka abecedy), obsahující
                       četnosti přechodů mezi znaky. Pokud se určitý bigram nevyskytuje,
                       příslušná hodnota je nastavena na 1.
    """

    TM = transition_matrix_raw(bigrams)

    # Nahrazení nul hodnotou 1
    TM[TM == 0] = 1

    return TM


def create_matrix_from_folder(folder_path):
    """
    Načte textové soubory ze složky, vytvoří bigramy ze všech souborů dohromady a na
    jejich základě sestaví bigramovou přechodovou matici. Předpokládá validní vstupní data.

    Args:
        folder_path (str): Cesta ke složce, která obsahuje textové soubory
                           určené ke zpracování.

    Returns:
        numpy.ndarray: Matice přechodů vytvořená z bigramů napříč všemi soubory ve složce.
    """

    all_bigrams = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        bigrams = get_bigrams(text)
        all_bigrams.extend(bigrams)

    return transition_matrix(all_bigrams)


def normalize_matrix(matrix):
    """
    Normalizuje číselnou matici tak, aby součet všech jejích prvků byl roven 1.
    Předpokládá, že součet matice není roven 0.

    Args:
        matrix (numpy.ndarray): Vstupní matice přechodů.

    Returns:
        numpy.ndarray: Normalizovaná matice, ve které každý prvek představuje relativní četnost
                       vůči celkovému součtu všech prvků v původní matici.
    """

    return matrix / np.sum(matrix)


def save_matrix(matrix, file_path):
    """
    Uloží bigramovou matici do CSV souboru ve formátu celých čísel.

    Args:
        matrix (numpy.ndarray): Matice, která bude uložena do souboru.
        file_path (str): Cesta k výstupnímu CSV souboru, do kterého se matice zapíše.

    Returns:
        None
    """

    np.savetxt(file_path, matrix, delimiter=",", fmt="%d")


def load_matrix(file_path):
    """
    Načte bigramovou (nebo jinou číselnou) matici z CSV souboru.

    Args:
        file_path (str): Cesta k CSV souboru, ze kterého se matice načte.

    Returns:
        numpy.ndarray: Načtená matice jako pole typu int.
    """

    return np.loadtxt(file_path, delimiter=",", dtype=int)


if __name__ == "__main__":
    """
    Ukázka funkcí pro práci s maticemi.
    """

    #print("Vytvářím a ukládám matici...")

    # Vytvoření matice
    # matrix = create_matrix_from_folder(DOWNLOAD_DIR)

    # Uložení do souboru
    #save_matrix(matrix, MATRIX_PATH)

    # Načtení a ověření
    loaded_matrix = load_matrix(MATRIX_PATH)

    print("")
    print("uložená matice:")
    print(loaded_matrix)

    print("")
    print("Normalizovaná matice:")
    print(normalize_matrix(loaded_matrix))
