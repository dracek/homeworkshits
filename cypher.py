import os
import numpy as np
import random

from config import alphabet
from bigrams import get_bigrams, transition_matrix, normalize_matrix, load_matrix




def substitute_encrypt(plaintext, key):
    """
    Provede substituční šifrování daného textu pomocí klíče.

    :param plaintext: Text k zašifrování
    :param key: Odpovídající znaky v šifrovací abecedě
    :return: Zašifrovaný text
    """
    # Vytvoření mapování znaků
    mapping = {alphabet[i]: key[i] for i in range(len(alphabet))}

    # Šifrování textu
    encrypted_text = ''.join(mapping[char] if char in mapping else char for char in plaintext)

    return encrypted_text


def substitute_decrypt(ciphertext, key):
    """
    Provede dešifrování substituční šifry pomocí klíče.

    :param ciphertext: Zašifrovaný text
    :param key: Odpovídající znaky v šifrovací abecedě
    :return: Dešifrovaný text
    """
    # Vytvoření inverzního mapování znaků
    reverse_mapping = {key[i]: alphabet[i] for i in range(len(alphabet))}

    # Dešifrování textu
    decrypted_text = ''.join(reverse_mapping[char] if char in reverse_mapping else char for char in ciphertext)

    return decrypted_text


def plausibility(text, TM_ref):
    """
    Vypočítá pravděpodobnost textu na základě referenční bigramové matice.

    :param text: Vstupní text
    :param TM_ref: Referenční bigramová matice (normalizovaná)
    :return: Pravděpodobnostní skóre textu
    """
    bigrams_obs = get_bigrams(text)  # Získání bigramů z textu
    TM_obs = transition_matrix(bigrams_obs)  # Vytvoření matice bigramů


    # hmm? todo
    TM_ref[TM_ref == 0] = 1

    likelihood = 0
    n = len(alphabet)

    for i in range(n):
        for j in range(n):
            if TM_ref[i][j] > 0:  # Abychom se vyhnuli log(0)
                likelihood += np.log(TM_ref[i][j]) * TM_obs[i][j]

    return likelihood


def plausibility2(text, TM_ref):
    """Vyhodnocuje pravděpodobnost textu pomocí bigramové matice."""
    bigrams_obs = get_bigrams(text)
    TM_obs = transition_matrix(bigrams_obs)
    return np.sum(np.log(TM_ref) * TM_obs)


def prolom_substitute(text, TM_ref, iterations, start_key):
    """
    Provádí substituční dešifrování pomocí simulovaného žíhání.

    :param text: Šifrovaný text
    :param TM_ref: Referenční bigramová matice (normalizovaná)
    :param iterations: Počet iterací algoritmu
    :param start_key: Počáteční klíč pro substituci
    :return: Nejlepší nalezený dešifrovaný text a odpovídající klíč
    """
    current_key = list(start_key)  # Počáteční klíč jako seznam znaků
    decrypted_current = substitute_decrypt(text, current_key)
    p_current = plausibility(decrypted_current, TM_ref)

    for i in range(iterations):
        candidate_key = current_key[:]  # Kopie aktuálního klíče
        idx1, idx2 = random.sample(range(len(alphabet)), 2)  # Vybereme dva náhodné indexy
        candidate_key[idx1], candidate_key[idx2] = candidate_key[idx2], candidate_key[idx1]  # Prohodíme znaky

        decrypted_candidate = substitute_decrypt(text, candidate_key)
        p_candidate = plausibility(decrypted_candidate, TM_ref)

        q = p_candidate / p_current if p_current != 0 else 0

        if q > 1 or random.uniform(0, 1) < 0.01:
            current_key = candidate_key
            p_current = p_candidate

        if i % 50 == 0:
            print(f"Iteration {i}, log plausibility: {p_current}")

    best_decrypted_text = substitute_decrypt(text, current_key)
    return (current_key, best_decrypted_text, p_current)


def prolom_substitutex(text, TM_ref, iter=1000, start_key=None):
    """Prolomí substituční šifru pomocí Metropolis-Hastings algoritmu."""
    if start_key is None:
        start_key = random.sample(alphabet, len(alphabet))  # Náhodná permutace

    current_key = start_key
    decrypted_current = substitute_decrypt(text, current_key)
    p_current = plausibility(decrypted_current, TM_ref)

    for i in range(iter):
        # Náhodná změna klíče
        candidate_key = current_key[:]
        i1, i2 = random.sample(range(len(alphabet)), 2)
        candidate_key[i1], candidate_key[i2] = candidate_key[i2], candidate_key[i1]

        # Vyhodnocení pravděpodobnosti
        decrypted_candidate = substitute_decrypt(text, candidate_key)
        p_candidate = plausibility(decrypted_candidate, TM_ref)

        # Přijímací pravděpodobnost
        if(p_candidate - p_current > 700):                                          #                       todo clip!  x = np.minimum(x, 700)
            print(p_candidate, p_current)
        q = np.exp(p_candidate - p_current)

        if q > 1 or random.uniform(0, 1) < q:
            current_key = candidate_key
            p_current = p_candidate

        # Výpis každých 50 iterací
        if i % 50 == 0:
            print(f"Iterace {i}: Log likelihood: {p_current}")

    return current_key, substitute_decrypt(text, current_key)

if __name__ == "__main__":

    print("Encrypt:")

    txt1 = "_VOZEM_DO_NEHO_A_ZAS_MNE_BEZI_DO_CESTY__ZACHVELA_SE_TAK_KUDY_VPRAVO_NEBO_VLEVO_TEDY_JE_KONEC_PTAL_SE_TISE_POKYVLA_HLAVOU_TEDY_JE"
    txt2 = "ABM_DEAOMARDHMAVA_VNAERDALD_UAOMAZDNYPAA_VZHBDSVANDAYVWAWIOPABCKVBMARDLMABSDBMAYDOPAXDAWMRDZACYVSANDAYUNDACMWPBSVAHSVBMIAYDOPAXD"
    key = "VLZODTQHUXWSERMCFKNYIBJGP_A"

    print(substitute_encrypt(txt1, key))

    print("")
    print("Decrypt:")

    print(substitute_decrypt(txt2, key))


    print("")
    print("Likelihood:")

    ptext = "AHOJ_NAZDAR_ATD"
    MATRIX_PATH = os.path.join("resources", "bigram_matice.csv")

    TM_ref = normalize_matrix(load_matrix(MATRIX_PATH))

    likelihood = plausibility(ptext, TM_ref)
    print(likelihood)


    xtext = "XXXX_XXXXXX_XXX"
    #MATRIX_PATH = os.path.join("resources", "bigram_matice.csv")

    #TM_ref = normalize_matrix(load_matrix(MATRIX_PATH))

    likelihood = plausibility(xtext, TM_ref)
    print(likelihood)


    print("")
    print("Prolom:")

    iterations = 20_000
    start_key = "VLZODTQHUXWSERMCFKNYIBJGA_P"

    prolamovaci_text = "ABM_DEAOMARDHMAVA_VNAERDALD_UAOMAZDNYPAA_VZHBDSVANDAYVWAWIOPABCKVBMARDLMABSDBMAYDOPAXDAWMRDZACYVSANDAYUNDACMWPBSVAHSVBMIAYDOPAXDAWMRDZAMYDBKDSAOBUKWVABPNWMZUSA_ABM_IAVACMNYVBUSANDACKDOAWMSVAXDOAKDWSAZHKVCYUBDACMXDODNACKDNDAERDAIXDSVANABM_DEAOBVAWKMWPA_CDYACMXOAEINUEDAOVSAOMBD_IAYDAVNCMRALSU_AWAHKVRUZUEAWVEAZHZDNA_CVYWPANWKUCDSA_ILPA_CVYWPANAYDLMIANDAERMIARDRUAVRUAOMCKDOIAVRUA_CVYWPAZMCVWAEUARDKM_IEUNAEINUEAYMAIODSVYAVLPNABUODSAVLPALPSMAXUNYMA_DAXNDEAYDAEDSVAKVOVAEPNSUNA_DALPZHAEMHSVAXDNYDAXDORMIANSPNDYAZMNAEUAKDWSA_CVYWPARDEI_DNALIOALPNAEINDSABPOVYAYMAZMARDZHZDNAVARDNEUNARDLMALPAYDAMOBD_SUAVAXVAANCINYUSVAKIZDAOMAWSURVABUOUNAUARVAYMAXNDEAEPNSDSVA_DALPZHANSVANAYDLMIAOMCKDOIAOMBDOSVALPZHAYMAOMBDOSVALPZHAYMAXUNYDAVSDAAYPAXNUAYVEARDWODA_VNRMILDRAXOUAWARUAHSDOARUWOPAEDARDRVCVOSMACYVYANDAYDARVAYMAWOP_AXDAZSMBDWACKURZD_RVAEPNSUANUA_DAXDARVANBDYDANVEAEVNAXUAKVOACMHSDOSARVARUAIYKP_RDRPEVAMZUEVACKDZDAXDRARDOMBDOSA_VCKUYAAYVWABUOUNABPODZHSVAYPARDIEUNAVRUASHVYAYPAEUSPAVSDACMZHMCAWOP_AXNDEANUAYMACVW"

    print(prolom_substitutex(prolamovaci_text, TM_ref, iterations))

