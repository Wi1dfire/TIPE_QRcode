import fonctionsbase as fb

Q = [1,0,1,0,0,1,1,0,1,1,1] 
msq = [1,0,1,0,1,0,0,0,0,0,1,0,0,1,0]

def correctionbit(cor:list, mask:list) -> list:
    """calcul les bits de correction

    Args:
        cor (list): niveau de correction utilisé
        mask (list): mask utilisé

    Returns:
        list: bits de correction
    """
    data = cor + mask
    R = fb.retirezeros(data + [0]*10)
    while len(R) > 10:
        temp = Q.copy() + [0] * abs(len(R)-len(Q))
        R = fb.XORlist(R, temp)
        R = fb.retirezeros(R)
    return [0]*(10-len(R)) + R

def informationsformat(cor:list, mask:list) -> list:
    """retourne les informations de format

    Args:
        cor (list): niveau de correction utilisé
        mask (list): mask utilisé

    Returns:
        list: informations de format
    """
    return fb.XORlist(cor + mask + correctionbit(cor, mask),msq)

def recupinformat(L:list) -> list:
    """récupère les informations de format du QRcode

    Args:
        L (list): QRcode

    Returns:
        list: informations de format
    """
    info = []
    for i in range(9):
        info.append(L[i][8])
    for i in range(7, 15):
        info.append(L[8][14-i])
    info.pop(6)
    info.pop(9)
    return fb.XORlist(info[::-1], [1,0,1,0,1,0,0,0,0,0,1,0,0,1,0]) #on récupère les informations de format en appliquant le masque de format

def masqueinformat() -> list:
    """retourne le masque de format

    Returns:
        list: masque de format
    """
    return msq