def int_to_bits(n:int):
    """Transforme un entier en binaire

    Args:
        n (int): entier

    Returns:
        str: entier en binaire
    """
    return [int(i) for i in format(n, '08b')]

def str_to_bits(L:str):
    """Transforme une chaine de caractère en binaire

    Args:
        L (str): chaine de caractère

    Returns:
        list: liste en binaire
    """
    res = ""
    for i in range(len(L)):
        res += format(ord(L[i]), '08b')
    return [int(i) for i in res]

def bitstooctet(L:list):
    """Transforme une liste de bits en octet

    Args:
        L (list): liste de bits

    Returns:
        list: liste d'octets
    """
    octet = []
    for i in range(0, len(L), 8):
        byte = int("".join(map(str, L[i:i+8])), 2)
        octet.append(byte)
    return octet

def inttooctet(n:int):
    """Transforme un entier en octet

    Args:
        n (int): entier

    Returns:
        list: octet
    """
    return bitstooctet(int_to_bits(n))

def strtooctet(L:str):
    """Transforme une chaine de caractère en octet

    Args:
        L (str): chaine de caractère

    Returns:
        list: liste d'octets
    """
    return bitstooctet(str_to_bits(L))

def strtolist(L:str):
    """Transforme une chaine de caractère en liste

    Args:
        L (str): chaine de caractère

    Returns:
        list: liste
    """
    return [i for i in L]