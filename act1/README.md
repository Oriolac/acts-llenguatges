# Com s'utilitza
## Lex
  Tots els exercicis estan fets amb lex i es poden executar mitjançant la comanda:
    `make`
    `./pX.l`
  on X és el nombre de l'exercici que es vol executar. Per exemple, si es vol 
  executar l'exercici 1 s'hauria de fer:
    `make`
    `./p1.l`
  També es pot utilitzar la comanda `make tests` per executar tots els tests a l'hora,
  o `make test` per seleccionar-ne un en específic.
  
## Python
  Els exercicis 2 i 3 a més a més d'estar fets amb lex també hi ha una implementació amb PLY.
  Per executar-ho és necessari tenir ply instal·lat al sistema (veure requeriments.txt) i executar
  la següent comanda:
    `python pX.py < in_file`
  on X és el nombre de l'exercici que es vol executar. Per exemple, si es vol executar l'exerici 2
  s'hauria de fer:
    `python p2.py < test/ok.test`

  

# Exercici 1
  - keywords parser -> arxiu per keywords
  - Es tenen en compte les barres invertides '\' a les strings 

# Exercici 2
  - S'ha utilitzat un script en python per fer nosaltres les proves

# Exercici 3
  - Super semblant al 2

# Exercici 4
  - Mètode yywrap amb pila amb buffer
  - Especificar lexic macros i includes

# Exercici 5
  - Com es fa
  - Especificar lexic macro amb expansió
  - Només agafa paràmetres si estan entre espais 
    #define int(b) hola(b)
    #define int(b) hola( b )

