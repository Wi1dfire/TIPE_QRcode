import fonctionsbase as fb

Q = [1,1,1,1,1,0,0,1,0,0,1,0,1]

def correctionbit(version:list) -> list:
    """calcul les bits de correction

    Args:
        version (list): version du QRcode sous forme de liste de bits

    Returns:
        list: bits de correction
    """
    R = fb.retirezeros(version + [0]*12)
    while len(R) > 12:
        temp = Q.copy() + [0] * abs(len(R)-len(Q))
        R = fb.XORlist(R, temp)
        R = fb.retirezeros(R)
    return [0]*(12-len(R)) + R

def informationsversion(version:list) -> list:
    """retourne les informations de version

    Args:
        version (list): version du QRcode sous forme de liste de bits

    Returns:
        list: informations de version
    """
    return version + correctionbit(version)