# Pràctica 2
Fet per Oriol Alàs, Guillem Felis i Ian Palacín
## Execució

Tots els exercicis estan fets en PLY. Per executar-ho és necessari tenir ply instal·lat al sistema (veure requeriments.txt) i executar
la següent comanda:
`python pX.py < in_file`
A més a més, s'ha creat un fitxer *Makefile* i un programa python,  per executar uns tests.

## Exercicis

### Exercici 1

Es va decidir que en la nostra proposta, la calculadora no acceptés operacions entre diferents tipus (floats i enters), sinó que cada operació binària hagués de ser d'un mateix tipus.

S'ha creat un diccionari anomenat `binary_operations` que ens servirà per cridar al nostre.

Com que el llenguatge que accepta variables floats i el llenguatge que no accepta variables enteres no comparteix cap paraula, es pot guardar a la mateixa estructura de dades, que en el nostre cas també serà un diccionari.

### Exercici 2 

En aquest exercici, encara que PLY accepti diferents *rule functions* per especificació gramàtica, en aquest cas s'ha optat utilitzar la forma convencional i posar condicionals per saber el que s'ha de fer en cada cas. Em cas que hi hagi parèntesis, posar la expressió sense; en cas que sigui un enter, posar el valor i, en cas que sigui la operació, canviar la sintaxis a posfixa.

### Exercici 3

En aquest exercici, en lloc de retornar en cada terminal una String, s'haurà de retornar una classe que contingui el valor de si té parentesis, per tal de saber si s'ha de treure o no. S'ha de treure en els següents casos:

* En cas que la expressió sigui un enter: `( INT )`
* En cas que hi hagi un parèntesis anidat: `( ( expr ) )`
* En cas que la operació anidada sigui d'igual o anterior prioritat a l'exterior.

### Exercici 4

Per tal de realitzar aquest exercici, primer, s'ha copiat el procediment de com es crea cada construcció gramàtica en un autòmat utilitzant el procediment de thompson. Per cada construcció s'ha creat una *rule function* per tenir el codi de manera més organitzat. A més a més, s'ha intentat optimitzar algunes operacions per tal de no sobre-carregar el autòmat d'estat lambda.

### Exercici 5 i 6

Per l'exercici 5, només es necessitava fer el canvi entre implicació i doble implicació, qual cosa no era molt difícil gràcies a l'experiència adquirida fent els anteriors programes. No obstant això, l'exercici 6 requeria un punt de vista més analític. Per tal de resoldre aquest problema, s'ha generat una estructura de arbre amb nodes que podien ser:

* SymbolNode on el seu valor era el símbol d'una variable.
* PNode representant els parèntesis encapsulats dintre d'una expressió, sent aquesta el valor daquest node.
* BinaryNode representant una operació binaria entre dos altres nodes.
* NegNode representant la negació sobre una expressió.

Un cop creat l'arbre, es realitza un recorregut preordre per cada operació que es vol realitzar.
Primer, s'ha realitzat la propagació de negacions, ja que d'aquesta manera s'estalvia haver de tenir un cas més en la eliminació de parèntesis que no alterin prioritat de la expressió. La propagació es realitza només quan es troba un node de negació i el seu node fill no és un símbol. En cas que es trobi un node de negació i hi hagi una propagació de negació anterior, es para la propagació però es continua recorrent tot l'arbre.
Per treure els parèntesis, es fa també un recorregut preordre que va seguint els diferents casos explicats en l'exercici 3.
