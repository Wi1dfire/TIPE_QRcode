def mask_000(L, interdit) -> None:
    """applique le masque 000 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and j%3 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_001(L, interdit) -> None:
    """applique le masque 001 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and (i+j)%3 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_010(L, interdit) -> None:
    """applique le masque 010 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and (i+j)%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_011(L, interdit) -> None:
    """applique le masque 011 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and i%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_100(L, interdit) -> None:
    """applique le masque 100 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and ((i*j)%3+i*j)%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_101(L, interdit) -> None:
    """applique le masque 101 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and ((i*j)%3+i+j)%2 == 0 :
                L[i][j] = (L[i][j] + 1) % 2

def mask_110(L, interdit) -> None:
    """applique le masque 110 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and (i/2+j/3)%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_111(L, interdit) -> None:
    """applique le masque 111 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and (i*j)%3+(i*j)%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def appli(L, mask, interdit) -> None:
    """applique le masque voulut au QRcode

    Args:
        L (list): Qrcode
        mask (int): masque souhaité
        interdit (list): liste des cases interdites à donner en argument à la fonction masque
    """
    if mask == 0:
        mask_000(L, interdit)
    if mask == 1:
        mask_001(L, interdit)
    if mask == 10:
        mask_010(L, interdit)
    if mask == 11:
        mask_011(L, interdit)
    if mask == 100:
        mask_100(L, interdit)
    if mask == 101:
        mask_101(L, interdit)
    if mask == 110:
        mask_110(L, interdit)
    if mask == 111:
        mask_111(L, interdit)
