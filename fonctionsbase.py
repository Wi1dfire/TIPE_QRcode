def retourne_octet(L:list) -> None:
    """retourne un liste (en place). En place

    Args:
        L (list): liste à retourner 
    """
    for i in range (len(L)//2):
        L[i],L[-1-i] = L[-1-i],L[i]

def int_to_bits(n:int) -> list:
    """Transforme un entier en binaire

    Args:
        n (int): entier

    Returns:
        list: entier en binaire
    """
    return [int(i) for i in format(n, '08b')]

def str_to_bits(L:str) -> list:
    """Transforme une chaine de caractère en binaire avec la table Unicode

    Args:
        L (str): chaine de caractère

    Returns:
        list: liste en binaire
    """
    res = ""
    for i in range(len(L)):
        res += format(ord(L[i]), '08b')
    return [int(i) for i in res]

def bits_to_str(L:list) -> str:
    """Transforme une liste de bits en chaine de caractère

    Args:
        L (list): liste de bits

    Returns:
        str: chaine de caractère
    """
    res = ""
    for i in range(0, len(L), 8):
        byte = int("".join(map(str, L[i:i+8])), 2)
        res += chr(byte)
    return res

def bitstolist(L:list) -> list:
    """Transforme une liste de bits en liste d'entiers

    Args:
        L (list): liste de bits

    Returns:
        list: liste d'entiers
    """
    octet = []
    for i in range(0, len(L), 8):
        byte = int("".join(map(str, L[i:i+8])), 2)
        octet.append(byte)
    return octet

def strtolist(L:str) -> list:
    """Transforme une chaine de caractère en liste d'entier

    Args:
        L (str): chaine de caractère

    Returns:
        list: liste d'entier
    """
    return bitstolist(str_to_bits(L))

def octetstoliste(L:list) -> list:
    """transforme une liste d'octets (sous forme de liste) en une liste de bits
    En place mais le return permet une utilisation plus facile.

    Args:
        L (list): liste d'octets à convertir

    Returns:
        list: liste des bits (octets mis bout à bout dans une liste)
    """
    Données = []
    for i in range (len(L)):
        octet = L[i].copy()
        for j in range (len(octet)):
            Données.append(octet[j])
    return Données

def listtobits(L:list) -> list:
    """Transforme une liste d'octets en liste de bits

    Args:
        L (list): liste d'octets

    Returns:
        list: liste de bits
    """
    Données = []
    for i in range (len(L)):
        Données += int_to_bits(L[i])
    return Données

def unique(L:list) -> list:
    """Retourne une liste sans doublon

    Args:
        L (list): liste

    Returns:
        list: liste sans doublon
    """
    return list(set(L))

def bitslisttoint(L:list) -> int:
    """convertit une liste de 8 bits en entier

    Args:
        L (list): liste de 8 bits

    Returns:
        int: entier en base 10
    """
    return sum([L[i]*2**(7-i) for i in range(len(L))])

def typeinfo(L:str) -> str:
    """Retourne le type d'information contenu dans une chaîne de caractères
    (numérique, alphanumérique, binaire ou kanji)

    Args:
        L (str): information

    Returns:
        str: type d'information
    """
    if all(c in '01' for c in L):
        return "binaire"
    if L.isnumeric():
        return "numérique"
    if all(c.isalnum() or c.isspace() or c in "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~" for c in L):
        return "alphanumérique"
    return "kanji"

def retirezeros(L:list) -> list:
    """retire les 0 de début de la liste 

    Args:
        L (list): liste à traiter

    Returns:
        list: liste sans 0 au début
    """
    while L and L[0] == 0:
        L.pop(0)
    return L

def XORlist(L1:list, L2:list) -> list:
    """Effectue un XOR entre deux listes de bits

    Args:
        L1 (list): liste 1
        L2 (list): liste 2

    Returns:
        list: liste de bits résultante
    """
    assert len(L1) == len(L2), "Les listes doivent avoir la même longueur"
    return [(a + b) % 2 for a, b in zip(L1, L2)]

def strbtolistb(L:str) -> list:
    """Transforme une chaîne de charatère de bits en liste de bits

    Args:
        L (str): chaîne de charatère de bits

    Returns:
        list: liste de bits
    """
    return [1 if i == "1" else 0 for i in L]

def complementaire(L:list) -> list:
    """Retourne le complémentaire d'une liste de bits 
    (1 devient 0 et 0 devient 1)

    Args:
        L (list): liste de bits

    Returns:
        list: complémentaire de la liste de bits
    """
    return [(1 + i) % 2 for i in L ]