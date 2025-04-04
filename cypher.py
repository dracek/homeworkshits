alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"


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


if __name__ == "__main__":

    print("Encrypt:")

    txt1 = "_VOZEM_DO_NEHO_A_ZAS_MNE_BEZI_DO_CESTY__ZACHVELA_SE_TAK_KUDY_VPRAVO_NEBO_VLEVO_TEDY_JE_KONEC_PTAL_SE_TISE_POKYVLA_HLAVOU_TEDY_JE"
    txt2 = "ABM_DEAOMARDHMAVA_VNAERDALD_UAOMAZDNYPAA_VZHBDSVANDAYVWAWIOPABCKVBMARDLMABSDBMAYDOPAXDAWMRDZACYVSANDAYUNDACMWPBSVAHSVBMIAYDOPAXD"
    key = "VLZODTQHUXWSERMCFKNYIBJGP_A"

    print(substitute_encrypt(txt1, key))

    print("")
    print("Decrypt:")

    print(substitute_decrypt(txt2, key))