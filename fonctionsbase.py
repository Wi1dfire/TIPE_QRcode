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
        str: entier en binaire
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