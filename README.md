# homeworkshits

## JAK TO FUNGUJE:

**download_resources.py** - stahuje data knih z wikisource. Data nejsou přiložena v gitu.

**bigrams.py** - práce s maticemi. Ukládají se nenormalizované, aby byly hezky v celých číslech. Funkce transition_matrix_raw() se používá pro TM_obs, u které umělé nafukování jedničkami zhoršuje výsledky. 

**cypher.py** - samotná práce se šiframi, ukázka prolomení

**decipher_all.py** - hromadné dešifrování, nebude součástí knihovny, ale funkcionalitu budete potřebovat


## TO DO:

 - upatlat z toho knihovnu
 - a celý ten jupyter notebook


## implementované a zdokumentované funkce požadované v zadání 
  - **get_bigrams(text)✅**
  - **transition_matrix(bigrams)✅**
  - **substitute_encrypt(plaintext, key)✅**
  - **substitute_decrypt(ciphertext, key)✅**
  - **prolom_substitute(text, TM_ref, iter, start_key)✅**
  - **plausibility(text, TM_ref)✅**


## parametry 
  - alphabet- obsahuje abecedu písmen, např. list 
  - TM_ref – referenční relativní matice bigramů / přechodů sestavená z nějakého textu který není zašifrovaný (např. knihy) 
  - iter – počet iterací algoritmu 
  - start_key  - dává uzivatel ale pokud ho nedá vygenerujte náhodně počáteční klíč pro prolomení šifry. 
  - text – zašifrovaný text se kterým pracujeme 