# homeworkshits

## DONE:

1) nasosání dat z wikipedie, transformace a uložení
2) bigramová matice - vytvoření, uložení, normalizace
3) encrypt a decrypt funkce
4) prolomení šifry

implementované funkce
  - **get_bigrams(text)✅**
  - **transition_matrix(bigrams)✅**
  - **substitute_encrypt(plaintext, key)✅**
  - **substitute_decrypt(ciphertext, key)✅**
  - **prolom_substitute(text, TM_ref, iter, start_key)✅**
  - **plausibility(text, TM_ref)✅**

vyleštění kódu
  - **download_resources.py✅**


## TO DO:

1) hromadné prolamování zadaných zdrojů
2) vyleštit kód



## parametry 
  - alphabet- obsahuje abecedu písmen, např. list 
  - TM_ref – referenční relativní matice bigramů /přechodů sestavená z nějakého textu který není zašifrovaný (např. knihy) 
  - iter – počet iterací algoritmu 
  - start_key  - dává uzivatel ale pokud ho nedá vygenerujte náhodně počáteční klíč pro prolomení šifry. 
  - Text – zašifrovaný text se kterým pracujeme 