# homeworkshits

## DONE:

1) nasosání dat z wikipedie, transformace a uložení

2) bigramová matice - vytvoření, uložení, normalizace



funkce
  - **get_bigrams(text)**
  - **transition_matrix(bigrams)**


## TO DO:

1) zbytek :P

funkce
  - prolom_substitute(text, TM_ref, iter, start_key)
  - plausibility(text, TM_ref)
  - substitute_encrypt(plaintext, key)
  - substitute_decrypt(ciphertext, key)



parametry 
  - alphabet- obsahuje abecedu písmen, např. list 
  - TM_ref – referenční relativní matice bigramů /přechodů sestavená z nějakého textu který není zašifrovaný (např. knihy) 
  - iter – počet iterací algoritmu 
  - start_key  - dává uzivatel ale pokud ho nedá vygenerujte náhodně počáteční klíč pro prolomení šifry. 
  - Text – zašifrovaný text se kterým pracujeme 