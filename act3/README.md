
# Especificacions del llenguatge

## Introducció

Per tal d'executar el programa, s'usa la comanda:

```sh
python main.py <fitxer>
```

A continuació, s'introduirà el lèxic i al sintaxis del llenguatge.

Hi ha un delimitador de línea, sent aquest el ';'. Aquest només caldrà per les assignacions i les crides a funcions. El llenguatge accepta inferència de tipus menys a la declaració de funcions. Per aquest motiu, no es permet declarar una variable sense haver-la assignat. D'aquesta manera, el compilador sabrà destacar 4 tipus específics:

- Tipus condicional (Boolean)
- Tipus caràcter (Char)
- Tipus enter (Integer)
- Tipus de punt flotant (Float)

Com a relaxació del llenguatge, les operacions acoplades al llenguatge venen restringides pels tipus dels operants, de manera que hi ha operacions per enters, floats, booleans i caràcters de manera individual i restrictiva, és a dir, no es permet fer operacions entre els diferents tipus, només sent els enters i els floats els únics tipus que permeten operacions entre ells. La seva declaració i assignació és.

S'ha creat les llistes de manera que es poden fer multidimensionals i en una sola línea, tal que:

```sh
a = [[[2], [4, 5]], [[4, 5], [6, 7]], [[3.3], [2.5, 3]]];
```

No obstant això, tots els elements d'una llista han de ser d'un tipus o d'un tipus que heredin, com és el cas de Float i Integer, que hereden del tipus Num.

La definició de funcions està feta de tal forma:

```sh
funk <tipus_funcio> <nom_funcio> (<tipus_arg1>: <nom_arg1>, ..., <tipus_argn>: <nom_argn> ){
    <sentence1>
    <sentence2>
    ...
    <sentencen>
    retrunk <expr>;
}
```

Es permet la definició de funcions i la crida d'elles a dintre de funcions. D'aquesta manera ens aproximem a un llenguatge més modern com python, el qual també ho permet. S'havia pensat poder realitzar concatenacions de funcions però s'ha deixat per en futur pròxim.
Pel que fa les estructures bàsiques, s'han creat les següents:

- if

```sh
if <expr_cond> {
    <sentence1>
    <sentence2>
    ...
    <sentencen>
}
```

- if/else

```sh
if <expr_cond> {
    <sentence1>
    <sentence2>
    ...
    <sentencen>
} else {
    <sentence1>
    <sentence2>
    ...
    <sentencen>
}
```

- if/elif/else

```sh
if <expr_cond> {
    <sentence1>
    <sentence2>
    ...
    <sentencen>
} elif {
    <sentence1>
    <sentence2>
    ...
    <sentencen>
} else {
    <sentence1>
    <sentence2>
    ...
    <sentencen>
}
```

- if/elif

```sh
if <expr_cond> {
    <sentence1>
    <sentence2>
    ...
    <sentencen>
} elif <expr_cond> {
    <sentence1>
    <sentence2>
    ...
    <sentencen>
}
```

- for

```sh
for (<assignacio>, <expressio_cond>, <assignacio>) {
    <sentence1>
    <sentence2>
    ...
    <sentencen>
}
```

- while

```sh
while <expressio_cond> {
    <sentence1>
    <sentence2>
    ...
    <sentencen>
}
```

- repeat/until

```sh
repeat {
    <sentence1>
    <sentence2>
    ...
    <sentencen>
} until (<expressio_cond>)
```

## Funcionalitats i disseny

Per tal de decidir què surt per pantalla i quan, s'ha decidit crear una estructura d'arbre i, quan aquest arribi al node arrel, és a dir, en la terminal d'inici. D'aquesta manera, ha resultat molt fàcil, per exemple, establir la estructura *for*.

Per tal de tenir el codi més mantenible, s'ha decidit crear un paquet anomenat *computils* on inclogui una abstracció del que es necessita. D'aquesta manera, tenim els següents fitxers:

- En **exceptions.py** es guardaran totes les possibles excepcions, actualment només hi ha la excepció de complació: *CompileException*.
- En **expr.py** es guardarà les diferents dataclasses de Tipus i, a més a més, una classe anomenada Expr que ens guardarà el tipus i el valor on està aquella expressió. D'aquesta manera, es pot saber en tot moment i es pot manipular les variables temporals d'una manera més senzilla. A més a més, s'hi ha guardat el node de l'estructura d'arbre per fer una lectura més senzilla en el fitxer **main.py**.
- En **node.py** hi haurà la classe que ens representarà l'arbre i el qual podrem iterar finalment per mostrar per pantalla tot el que hi hagi en el seu contingut. La clase rep el mateix nom que el, Node. Aquest arbre serà un arbre binari el qual el seu recorregut serà pre-ordre. D'aquesta manera, podem establir de forma molt fàcil quin serà l'ordre de les sentències en el codi intermedi.
- En **stable.py** hi ha la implementació de la taula de simbols per tal de definir els àmbits de les variables. S'ha creat diferents àmbits en:
  - El cos de les funcions, ja que el bloc de codi és més independent i les variables noves en el bloc no ha d'afectar a un scope més global.
  - El cos dels condicionals, ja que potser no entra mai en el bloc de codi i hi ha noves variables assignades.
  - El cos dels bucles, per la mateixa raó que l'anterior.

## Tests

Per tal d'agilitzar i veure que funciona el nostre compilador, s'ha creat un makefile per la verificació de la nostra implementació i les seves funcionalitats. Només cal executar:

```sh
make
```

Fet per Oriol Alàs, Guillem Felis i Ian Palacín.