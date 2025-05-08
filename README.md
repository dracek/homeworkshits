# homeworkshits

## JAK TO FUNGUJE:

**download_resources.py** - stahuje data knih z wikisource. Data nejsou přiložena v gitu.

**bigrams.py** - práce s maticemi. Ukládají se nenormalizované, aby byly hezky v celých číslech. Funkce transition_matrix_raw() se používá pro TM_obs, u které umělé nafukování jedničkami zhoršuje výsledky. 



3) encrypt a decrypt funkce
4) prolomení šifry

## TO DO:

1) hromadné prolamování zadaných zdrojů
2) vyleštit kód

## implementované funkce
  - **get_bigrams(text)✅**
  - **transition_matrix(bigrams)✅**
  - **substitute_encrypt(plaintext, key)**
  - **substitute_decrypt(ciphertext, key)**
  - **prolom_substitute(text, TM_ref, iter, start_key)**
  - **plausibility(text, TM_ref)**

## vyleštění kódu
  - **download_resources.py✅**
  - **bigrams.py✅**
  - **cypher.py ❗️**




## parametry 
  - alphabet- obsahuje abecedu písmen, např. list 
  - TM_ref – referenční relativní matice bigramů / přechodů sestavená z nějakého textu který není zašifrovaný (např. knihy) 
  - iter – počet iterací algoritmu 
  - start_key  - dává uzivatel ale pokud ho nedá vygenerujte náhodně počáteční klíč pro prolomení šifry. 
  - text – zašifrovaný text se kterým pracujeme 