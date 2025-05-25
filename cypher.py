import os
import numpy as np
import random

from config import alphabet
from bigrams import get_bigrams, normalize_matrix, load_matrix, transition_matrix_raw


def substitute_encrypt(plaintext, key):
    """
    Provede substituční šifrování vstupního textu na základě zadaného klíče.

    Args:
        plaintext (str): Vstupní text, který má být zašifrován. Očekává se, že obsahuje pouze znaky z dané abecedy.
        key (str): Řetězec substitučního klíče. Měl by být permutací znaků abecedy.

    Returns:
        str: Text k zašifrování, kde každý znak z abecedy bude nahrazen odpovídajícím znakem z klíče.
    """

    # Vytvoření mapování znaků
    mapping = {alphabet[i]: key[i] for i in range(len(alphabet))}

    # Chyba při použití nepodporovaných znaků
    invalid_chars = set(plaintext) - set(alphabet)
    if invalid_chars:
        raise ValueError(f"Text obsahuje nepovolené znaky: {invalid_chars}")

    # Šifrování textu
    encrypted_text = ''.join(mapping[char] if char in mapping else char for char in plaintext)

    return encrypted_text


def substitute_decrypt(ciphertext, key):
    """
    Provede dešifrování substituční šifry na základě zadaného klíče.

    Args:
        ciphertext (str): Zašifrovaný text, který má být dešifrován. Očekává se, že obsahuje pouze znaky z klíče.
        key (list): Řetězec substitučního klíče, tj. permutace znaků abecedy, která byla použita při šifrování.

    Returns:
        str: Dešifrovaný text, ve kterém jsou znaky z klíče nahrazeny odpovídajícími znaky z původní abecedy.

    """
    # Vytvoření inverzního mapování znaků
    reverse_mapping = {key[i]: alphabet[i] for i in range(len(alphabet))}

    # Chyba při použití nepodporovaných znaků
    invalid_chars = set(ciphertext) - set(key)
    if invalid_chars:
        raise ValueError(f"Text obsahuje znaky, které nelze dešifrovat: {invalid_chars}")

    # Dešifrování textu
    decrypted_text = ''.join(reverse_mapping[char] if char in reverse_mapping else char for char in ciphertext)

    return decrypted_text


def plausibility(text, TM_ref):
    """
    Vypočítá pravděpodobnostní skóre textu na základě referenční bigramové matice.

    Args:
        text (str): Vstupní text, jehož jazyková přirozenost se hodnotí.
        TM_ref (numpy.ndarray): Normalizovaná referenční bigramová matice (pravděpodobnostní přechodová matice).

    Returns:
        float: Pravděpodobnostní skóre textu. Vyšší hodnota značí vyšší jazykovou pravděpodobnost vůči referenčnímu modelu.
    """

    bigrams_obs = get_bigrams(text)  # Získání bigramů z textu
    TM_obs = transition_matrix_raw(bigrams_obs)  # Vytvoření matice bigramů

    likelihood = 0
    n = len(alphabet)

    for i in range(n):
        for j in range(n):
            if TM_ref[i][j] > 0:  # Abychom se vyhnuli log(0)
                likelihood += np.log(TM_ref[i][j]) * TM_obs[i][j]

    return likelihood


def prolom_substitute(text, TM_ref, iterations, start_key = None):
    """
    Provede dešifrování substituční šifry pomocí metody simulovaného žíhání.

    Args:
        text (str): Šifrovaný text.
        TM_ref (numpy.ndarray): Normalizovaná referenční bigramová matice.
        iterations (int): Počet iterací algoritmu.
        start_key (list | None): Volitelný počáteční substituční klíč jako seznam znaků. Pokud není zadán, vygeneruje se náhodně.

    Returns:
        tuple[list[str], str, float]: Trojice obsahující:
            - nejlepší nalezený klíč (seznam znaků),
            - odpovídající dešifrovaný text,
            - jeho logaritmické pravděpodobnostní skóre (plausibility).
    """

    if start_key is None:
        current_key = list(alphabet)
        random.shuffle(current_key)
    else:
        current_key = list(start_key)  # Počáteční klíč jako seznam znaků

    decrypted_current = substitute_decrypt(text, current_key)
    p_current = plausibility(decrypted_current, TM_ref)

    # pamatujeme si nejlepší řešení
    p_best = p_current
    k_best = current_key

    for i in range(iterations):
        candidate_key = current_key[:]  # Kopie aktuálního klíče
        idx1, idx2 = random.sample(range(len(alphabet)), 2)  # Vybereme dva náhodné indexy
        candidate_key[idx1], candidate_key[idx2] = candidate_key[idx2], candidate_key[idx1]  # Prohodíme znaky

        decrypted_candidate = substitute_decrypt(text, candidate_key)
        p_candidate = plausibility(decrypted_candidate, TM_ref)

        q = p_candidate / p_current if p_current != 0 else 0

        # po normalizaci prvku matice jsou hodnoty 0 až 1, tim padem po jejich logaritmovani je hodnota plausability zaporna
        # přijímáme když je lepší p_candidate než p_current, tedy q < 1
        if q < 1 or random.uniform(0, 1) < 0.01:
            current_key = candidate_key
            p_current = p_candidate

            if p_best < p_current:
                p_best = p_current
                k_best = current_key

        if i % 1000 == 0:
            print(f"Iteration {i}, current plausibility: {p_current}")

        # občasný reset klíče, aby se dlouho nezůstával odchýlený od lepšího řešení
        if i % 1000 == 0:
            p_current = p_best
            current_key = k_best

    # vracíme nejlepší řešení, nikoliv poslední, protože s malou pravděpodobností i zhoršení a poslední řešení nemusí být nejlepsí
    best_decrypted_text = substitute_decrypt(text, k_best)
    return k_best, best_decrypted_text, p_best


if __name__ == "__main__":

    print("Test encrypt:")

    txt1 = "_VOZEM_DO_NEHO_A_ZAS_MNE_BEZI_DO_CESTY__ZACHVELA_SE_TAK_KUDY_VPRAVO_NEBO_VLEVO_TEDY_JE_KONEC_PTAL_SE_TISE_POKYVLA_HLAVOU_TEDY_JE"
    txt2 = "ABM_DEAOMARDHMAVA_VNAERDALD_UAOMAZDNYPAA_VZHBDSVANDAYVWAWIOPABCKVBMARDLMABSDBMAYDOPAXDAWMRDZACYVSANDAYUNDACMWPBSVAHSVBMIAYDOPAXD"
    key = "VLZODTQHUXWSERMCFKNYIBJGP_A"

    print(substitute_encrypt(txt1, key))

    print("")
    print("Test encrypt:")

    print(substitute_decrypt(txt2, key))


    MATRIX_PATH = os.path.join("resources", "bigram_matice.csv")

    TM_ref = normalize_matrix(load_matrix(MATRIX_PATH))

    #print("")
    #print("Test likelihood:")

    #ptext = "AHOJ_NAZDAR_NEJAY_TEST_ATD"
    #likelihood = plausibility(ptext, TM_ref)
    #print(likelihood)

    print("")
    print("Test prolom:")

    iterations = 20_000

    prolamovaci_text = "ABM_DEAOMARDHMAVA_VNAERDALD_UAOMAZDNYPAA_VZHBDSVANDAYVWAWIOPABCKVBMARDLMABSDBMAYDOPAXDAWMRDZACYVSANDAYUNDACMWPBSVAHSVBMIAYDOPAXDAWMRDZAMYDBKDSAOBUKWVABPNWMZUSA_ABM_IAVACMNYVBUSANDACKDOAWMSVAXDOAKDWSAZHKVCYUBDACMXDODNACKDNDAERDAIXDSVANABM_DEAOBVAWKMWPA_CDYACMXOAEINUEDAOVSAOMBD_IAYDAVNCMRALSU_AWAHKVRUZUEAWVEAZHZDNA_CVYWPANWKUCDSA_ILPA_CVYWPANAYDLMIANDAERMIARDRUAVRUAOMCKDOIAVRUA_CVYWPAZMCVWAEUARDKM_IEUNAEINUEAYMAIODSVYAVLPNABUODSAVLPALPSMAXUNYMA_DAXNDEAYDAEDSVAKVOVAEPNSUNA_DALPZHAEMHSVAXDNYDAXDORMIANSPNDYAZMNAEUAKDWSA_CVYWPARDEI_DNALIOALPNAEINDSABPOVYAYMAZMARDZHZDNAVARDNEUNARDLMALPAYDAMOBD_SUAVAXVAANCINYUSVAKIZDAOMAWSURVABUOUNAUARVAYMAXNDEAEPNSDSVA_DALPZHANSVANAYDLMIAOMCKDOIAOMBDOSVALPZHAYMAOMBDOSVALPZHAYMAXUNYDAVSDAAYPAXNUAYVEARDWODA_VNRMILDRAXOUAWARUAHSDOARUWOPAEDARDRVCVOSMACYVYANDAYDARVAYMAWOP_AXDAZSMBDWACKURZD_RVAEPNSUANUA_DAXDARVANBDYDANVEAEVNAXUAKVOACMHSDOSARVARUAIYKP_RDRPEVAMZUEVACKDZDAXDRARDOMBDOSA_VCKUYAAYVWABUOUNABPODZHSVAYPARDIEUNAVRUASHVYAYPAEUSPAVSDACMZHMCAWOP_AXNDEANUAYMACVW"

    k_best, best_decrypted_text, p_best = prolom_substitute(prolamovaci_text, TM_ref, iterations)

    print("")
    print("Best text:")
    print(best_decrypted_text)

