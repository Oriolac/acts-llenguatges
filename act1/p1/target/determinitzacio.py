#!/usr/bin/env python3

import automat

def list_without_none(list):
    """ Retorna una llista sense valors buits com: '' """
    result = []
    for element in list:
        if element:
            result.append(element)
    return result


def remove_duplicats(list):
    """ Retorna una llista sense valors repetits"""
    new_list = []
    for element in list:
        if element not in new_list:
            new_list.append(element)
    return new_list

def get_estats():
    """ Retorna els noms dels estats en una llista """
    estats = input('Introdueix els estats separats per un espai: ')
    # estats tindrà la forma: 'q0 q1'

    estats = estats.split(' ')
    # estats tindra la forma: ['q0', 'q1']

    estats = list_without_none(estats)
    # si estats era de la forma ['', 'q0'] passarà a la forma ['q0']

    # si estats era de la forma ['q0', 'q1', 'q0'] passarà a la forma ['q0', 'q1']
    return remove_duplicats(estats)


def get_set_estats(cadena):
    """ Retorna els estats que hi ha donada una cadena de caràcters """
    estats = cadena.split(' ')
    for estat in estats:
        if estat not in ESTATS:
            print('ERROR al rebre els estats, l\'estat ' + estat + ' no existeix.')
            exit()

    # Si n'hi ha de duplicats, els treu
    return remove_duplicats(estats)


def get_transicions():
    """
    Retorna un diccionari on cada clau és un estat i el seu valor és una tupla del producte cartesià LLETRa x ESTAT
    """

    def get_transitions_correctly(list, llista_equips):
        """ Retorna la llista d'elements LLETRA x ESTAT """
        transicions = []
        for transicio in list:
            transicio = transicio.split(' ')
            transicio = list_without_none(transicio)
            # transició tindrà la forma: ['a', 'q1']

            if transicio[1] not in llista_equips:
                print('ERROR al rebre les transicions! L\'estat ' + transicio[1] + 'no existeix.')
                exit()
            transicions.append(transicio)
        return transicions

    print('\t----- TRANSICIONS -----')
    print('Utilitza l per lambda')
    llista_transicions = {}
    print('EXEMPLE: a q2, b q3')
    for estat in ESTATS:
        transicions = input('De l\'estat ' + estat + ' tenim les transicions: ')
        transicions = transicions.split(',')
        transicions = list_without_none(transicions)
        # transicions tindra la forma ['a q2', ' b q2']

        llista_transicions[estat] = get_transitions_correctly(transicions, ESTATS)
        # llista_transicions[estat] tindrà la forma: [['a', 'q1'], ['a', 'q2']]

    return llista_transicions


def nom_llista_estats(llista_estats):
    """ Retorna, donada una llista d'objectes de classe Estat, el seu nom corresponent. """
    llista_noms = []
    for nom_estat in llista_estats:
        llista_noms.append(nom_estat.nom)
    return llista_noms


def es_final(llista_estats):
    """ Donat una llista d'estats, només que un d'ells sigui final, retorna True. """
    for nom_estat in llista_estats:
        estat = AUTOMAT_ENTRADA.get_estat(nom_estat)
        if estat.final:
            return True
    return False


def ordenar_estats(llista_nom_estats):
    """ llista_nom_estats : ['1', '2', '3']"""

    for index in range(1, len(llista_nom_estats)):
        nom = llista_nom_estats[index]
        index2 = index
        while index2 >= 0 and ord(nom) < ord(llista_nom_estats[index2]):
            llista_nom_estats[index2+1] = llista_nom_estats[index]
            index2 -= 1
        llista_nom_estats[index2] = nom
    return llista_nom_estats



def get_transicions_dels_estats(estats):
    """
    Donada una llista d'estats, retorna totes les seves transicions. S'utilitza per trobar les
        transicions d'un estat conjunt d'altres estats
    Exemple1:
    transicio[q1] : [['a', 'q2'], ['b', 'q3']. ['l', 'q2']]
    transicio[q2] : [['a', 'q3'], ['b', 'q3']]
    get_transicions_dels_estats([ESTAT q1, ESTAT q2]) :
        {'a': ['q2', 'q3'], 'b' : ['q3']}
    En aquest cas, no retornarà la lletra 'l' ja que el paràmetre passat sera el conjunt d'estats.
    En cas que l'estat q3 tingués una lambda-transició, aquest s'ha d'incloure
    """

    transicions = {}
    while not estats == []:
        estat = estats[0]
        estat = AUTOMAT_ENTRADA.get_estat(estat)
        for lletra in estat.transicions:
            # En cas que sigui lambda, ja estarà a estats
            if not lletra.__eq__('l'):
                if lletra not in transicions.keys():
                    transicions[lletra] = []

                # Mirem tots els estats que pot portar la lletra, contant les lambda-transicions
                for estat_desti in estat.transicions[lletra]:
                    if estat_desti.nom not in transicions[lletra]:
                        transicions[lletra].append(estat_desti.nom)

                        # Mirem el conjunt d'estats que ens porta en lambda-transicions
                        estats_desti_l = estat_desti.to_lletra('l')
                        while not estats_desti_l == []:
                            estat_desti2 = estats_desti_l[0]

                            # En cas que s'hagi d'afegir, mirem si aquest també te lambda-transicions i
                            # l'afegim a estats de l que es necessiten tractar (estats_desti_l)
                            if estat_desti2.nom not in transicions[lletra]:
                                transicions[lletra].append(estat_desti2.nom)
                                estats_desti3 = estat_desti2.to_lletra('l')
                                estats_desti_l += estats_desti3
                            estats_desti_l = estats_desti_l[1:]
        estats = estats[1:]

    for lletra in transicions:
        # En el pitjor cas de tenir duplicats, els treiem
        transicions[lletra] = remove_duplicats(transicions[lletra])
        # Per no crear un nou estat que sigui el mateix, s'ordenaran
        transicions[lletra] = ordenar_estats(transicions[lletra])
    return transicions


def trobar_conjunt(estats_a_tractar):
    # En cas que hi hagi lambda-transicions, les hem d'afegir.

    conjunt_estats = []
    while not estats_a_tractar == []:
        estat = estats_a_tractar[0]
        estat = AUTOMAT_ENTRADA.get_estat(estat)

        if estat.nom not in conjunt_estats:
            conjunt_estats.append(estat.nom)
            estats_desti = estat.to_lletra('l')

            # Es tractaran tots aquells estats on estat amb lambda pugui anar-hi
            for estat_desti in estats_desti:
                estats_a_tractar.append(estat_desti.nom)
        estats_a_tractar = estats_a_tractar[1:]
    return conjunt_estats


def determinitzar():
    """ Procés de determinització """

    AUTOMAT_DETERMINITZAT = automat.Automat()

    def afegir_estat(llista_estats, inicial=False):
        """ Crea el nou estat de l'Automat determinitzat i les seves noves transicions"""
        if AUTOMAT_DETERMINITZAT.get_estat(str(llista_estats)) is not None:
            return 0

        estats_a_tractar = remove_duplicats(llista_estats)
        conjunt_estats = trobar_conjunt(estats_a_tractar)
        estat_a_afegir = str(conjunt_estats)
        final = es_final(conjunt_estats)
        AUTOMAT_DETERMINITZAT.afegir_estat(estat_a_afegir, final=final, inicial=inicial)

        transicions = get_transicions_dels_estats(conjunt_estats)

        for lletra in transicions:
            afegir_estat(transicions[lletra])
            AUTOMAT_DETERMINITZAT.afegir_transicio(estat_a_afegir, lletra, str(transicions[lletra]))

    def afegir_estat_buit():
        """ És important per determinitzar, afegir l'estat buit quan un estat no té una transició d'una lletra """
        AUTOMAT_DETERMINITZAT.afegir_estat('buit')
        for lletra in AUTOMAT_DETERMINITZAT.alphabet():
            AUTOMAT_DETERMINITZAT.afegir_transicio('buit', lletra, 'buit')

    nom_estats_inicials = nom_llista_estats(AUTOMAT_ENTRADA.get_estats_inicials())
    afegir_estat(nom_estats_inicials, inicial=True)

    # Mirem que tots els estats tinguin totes les transicions, en cas contrari s'afegeixen i s'envien al conjunt buit.
    for estat in AUTOMAT_DETERMINITZAT.get_all_estats():
        for lletra in AUTOMAT_DETERMINITZAT.alphabet():
            if lletra not in estat.transicions.keys():
                if AUTOMAT_DETERMINITZAT.get_estat('buit') is None:
                    afegir_estat_buit()
                AUTOMAT_DETERMINITZAT.afegir_transicio(estat.nom, lletra, 'buit')

    print('\t--- IMPRESSIO PER PANTALLA DE L\'AUTOMAT DETERMINITZAT---')
    AUTOMAT_DETERMINITZAT.show()

    # En cas de voler-lo utilitzar, el retornarem
    return AUTOMAT_DETERMINITZAT


if __name__ == "__main__":
    AUTOMAT_ENTRADA = automat.Automat()
    print('\t----- ESTATS -----')
    ESTATS = get_estats()
    for estat in ESTATS:
        AUTOMAT_ENTRADA.afegir_estat(estat)

    cadena_estats_inicials = input('Introdueix els estats inicials separats per un espai: ')
    ESTATS_INICIALS = get_set_estats(cadena_estats_inicials)
    for nom_inicial in ESTATS_INICIALS:
        estat_inicial = AUTOMAT_ENTRADA.get_estat(nom_inicial)
        estat_inicial.inicial = True

    cadena_estats_finals = input('Introdueix els estats finals separats per un espai: ')
    ESTATS_FINALS = get_set_estats(cadena_estats_finals)
    for nom_final in ESTATS_FINALS:
        estat_final = AUTOMAT_ENTRADA.get_estat(nom_final)
        estat_final.final = True

    TRANSICIONS = get_transicions()
    # TRANSICIONS té a forma {'q1': [['a', 'q1']. ['b', 'q2']]}
    for estat in TRANSICIONS:
        for transicio in TRANSICIONS[estat]:
            if not AUTOMAT_ENTRADA.is_there_transicio(estat, transicio[0], transicio[1]):
                AUTOMAT_ENTRADA.afegir_transicio(estat, transicio[0], transicio[1])

    ALFABET = AUTOMAT_ENTRADA.alphabet()
    print('L\'alfabet és ' + str(ALFABET))
    print('\t--- IMPRESSIO PER PANTALLA DE L\'AUTOMAT SENSE DETERMINITZAR---')
    AUTOMAT_ENTRADA.show()
    if not AUTOMAT_ENTRADA.is_determinista():
        determinitzar()
    else:
        print('L\'automat ja és determinista')
