# Pràctica 1


## Analitzadors

### Lex

  Tots els exercicis estan fets amb lex i es poden executar mitjançant la comanda:
    `make`
    `./pX.l`
  on X és el nombre de l'exercici que es vol executar. Per exemple, si es vol 
  executar l'exercici 1 s'hauria de fer:
    `make`
    `./p1`
  En cas de voler canviar la sortida estàndar, es pot realitzar:
  `./p1 < <fitxer.c>`
  També es pot utilitzar la comanda `make tests` per executar tots els tests a l'hora,
  o `make test` per seleccionar-ne un en específic.
  
### Python

  Els exercicis 2 i 3 a més a més d'estar fets amb lex també hi ha una implementació amb PLY.
  Per executar-ho és necessari tenir ply instal·lat al sistema (veure requeriments.txt) i executar
  la següent comanda:
    `python pX.py < in_file`
  on X és el nombre de l'exercici que es vol executar. Per exemple, si es vol executar l'exerici 2
  s'hauria de fer:
    `python p2.py < test/ok.test`

## Exercici 1

  - S'ha creat un generador de paraules claus per tal de ficar en el nostre analitzador totes les paraules de manera automàtica. S'ha decidit identificar una paraula clau com un token per tal d'agilitzar la lectura i quedar-se el més obert possible per modificacions en un futur.
  - En aquest analitzador, s'ha tingut en compte l'ús de les barres invertides abans de salt de línia en les strings. Exemple: 

```
" That's a  \
correct     \
string. "
```

## Exercici 2

- S'ha utilitzat un script en python `testgen.py` per crear les proves de manera automàtica.
- L'ús de literals en el PLY ha agilitzat la creació i la lectura de l'analitzador en python.

## Exercici 3

L'exercici 3 ha estat el més fàcil de tots ja que s'han adquirit els coneixements apresos en els exercicis anteriors i aquest tenia molt punts semblants amb el segon.

## Exercici 4

### Ús

```
make
./p4 <fitxer_in> <fitxer_out>
```

### Observacions

Per permetre la inclusió d'arxius, s'ha modificat el mètode yywrap, que ens permetrà controlar la pila i l'estat del buffer, per saber quan és el final d'arxiu.

- Lèxic:
  - Inclusió d'arxius:
    - `#include <nom_arxiu>`
  - Creació de macros
    - `#define <nom_macro> <valor_macro>`

Per veure si és una macro definida o no a l'hora de reemplaçar-la, es busca a la funció `find_key`, que itera sobre les macros ja definides per saber si concideix el nom en alguna de elles.

## Exercici 5

### Ús

```
make
./p4 <fitxer_in> <fitxer_out>
```

### Observacions

En aquest exercici, s'inclou l'anàlisi lèxic de l'exercici anterior.
  - La funció `find_key` passa a ser `find_const_key` ja que, només en aquesta funció només es buscaran les macros constants.
  - Lèxic:
    - `#define <nom_macro>(<arg1>, <arg2>, ..., <arg3>) <valor>`
    - arg = `\[a-zA-Z_][a-zA-Z0-9_]*\`
  - S'ha relaxat el problema de manera que només es transformen els paràmetres si estan en espais.
    - Cas on __no__ es reemplaçaria _b_: `#define int(b) hola(b)`
    - Cas on __sí__ es reemplaçaria _b_: `#define int(b) hola( b )`

 En aquesta sol·lució es distingeixen dos tipus de macros: les constants i les que tenen expansió de paràmetres. El procés que du a terme el tractament de les macro amb paràmetres 

1. La funció `find_func_key` buscarà les macros amb expansió per saber si coincideix. S'ha creat una estructura en específic (que no pot ocòrrer en un cas real, ja que l'identificador no serà agafat per l'analitzador lèxic) per tal de tractar en cas que no trobi cap macro. Si es troba, es passa al pas de substitució de paràmetres. En cas que no es trobi, s'imprimeix pel fitxer de sortida el text.
2. La substitució de paràmetres es prepara a la funció `transform_text` on transforma la string dels arguments en un vector on cada element és l'argument i, reemplaça els arguments donats pels arguments de la macro en el text.
3. En la funció `replace_words` és on es busca en cada paraula (delimitada per espais) del text i es reemplaça en cas de trobar-se. La substitució és realitza gràcies a la funció `replace_or_repeat_word`. Realment, el que es fa no és substituir el text donat per la macro sinó crear una altra string `result` per tal de poder reutilitzar-la.
4. La funció de reemplaçar o repetir, buscarà un match per l'argument donat i retornarà el paràmetre en què correspon la mateixa posició. D'aquesta manera, la sol·lució no es preocupa d'errors com:

```c
>#define macro(a, b, c) a > b > c
>macro(b, 2, 3)
2 > 2 > 3
```

El resultat correcte amb la nostra sol·lució és:

```c
b > 2 > 3
```

## Link

El contingut d'aquesta pràctica i les posteriors es podrà trobar en aquest [en aquest repositori](https://github.com/Oriolac/acts-llenguatges).