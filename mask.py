import evaluation as eval
import copy
import fonctionsbase as fb
import informationsformat as informat

def mask_000(L:list, interdit:list) -> None:
    """applique le masque 000 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and (i+j)%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_001(L:list, interdit:list) -> None:
    """applique le masque 001 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and i%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_010(L:list, interdit:list) -> None:
    """applique le masque 010 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and j%3 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_011(L:list, interdit:list) -> None:
    """applique le masque 011 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and (i+j)%3 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_100(L:list, interdit:list) -> None:
    """applique le masque 100 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and (i/2+j/3)%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_101(L:list, interdit:list) -> None:
    """applique le masque 101 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and (i*j)%3+(i*j)%2 == 0 :
                L[i][j] = (L[i][j] + 1) % 2

def mask_110(L:list, interdit:list) -> None:
    """applique le masque 100 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and ((i*j)%3+i*j)%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_111(L:list, interdit:list) -> None:
    """applique le masque 111 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and ((i*j)%3+i+j)%2 == 0 :
                L[i][j] = (L[i][j] + 1) % 2

def  appli(L:list, mask:int, interdit:list, cor:list) -> None:
    """applique le masque voulut au QRcode

    Args:
        L (list): Qrcode
        mask (int): masque souhaité
        interdit (list): liste des cases interdites à donner en argument à la fonction masque
        cor (list): niveau de correction
    """
    funcs = {0:mask_000, 1:mask_001, 10:mask_010, 11:mask_011, 100:mask_100, 101:mask_101, 110:mask_110, 111:mask_111}
    funcs.get(mask)(L, interdit)
    masque = fb.strbtolistb(("00"+str(mask))[-3:])
    info = informat.informationsformat(cor, masque)
    #on inscrit les informations de format
    m,n = -1, -1
    for i in range (9):
        if (i,8) != ((6,8)):
            L[i][8] = int(info[m])
            m -= 1
        if (8,-1-i) != (8,-9):
            L[8][-1-i] = int(info[n])
            n -= 1
    for i in range (8, len(info)+1):
        if (8,7-i+8) != (8,6):
            L[8][7-i+8] = int(info[m])
            m -= 1
        if (-7+i-8,8) != (-7,8) and (-7+i-8) != (0,6):
            L[-7+i-8][8] = int(info[n])
            n -= 1
        else :
            L[-7+i-8][8] = 1

def choix_mask(L:list, interdit:list, cor:list) -> int:
    """choisit le masque optimal pour le QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des cases interdites
        cor (list): liste du niveau de correction d'erreur

    Returns:
        int: masque optimal
    """
    score, mask = [], [0,1,10,11,100,101,110,111]
    for i in mask:
        test = copy.deepcopy(L)
        appli(test, i, interdit, cor)
        score.append(eval.evaluer(test))
    return mask[score.index(min(score))]

def score(L:list, c:list, cor:list) -> tuple[list,int]:
    """retourne le score de chaque masque

    Args:
        L (list): QRcode
        c (list): liste des cases interdites

    Returns:
        list: score de chaque masque
        int: masque avec le score minimal
    """
    score, mask = [], [0,1,10,11,100,101,110,111]
    for i in mask:
        test = copy.deepcopy(L)
        appli(test, i, c,cor)
        score.append(eval.evaluer(test))
    return score, mask[score.index(min(score))]

def maskoptimal(L:list, lvl:list, c:list) -> None:
    """applique le masque optimal au QRcode

    Args:
        L (list): QRcode
        lvl (int): niveau de correction
        version (int): version du QRcode.
    """
    U = [25, 7, 30, 15]
    cor = fb.strbtolistb(bin(U.index(lvl))[2:])
    cor = [0]*(2-len(cor)) + cor
    return appli(L, choix_mask(L,c,cor), c, cor)

def masque_utilise(L:list) -> int:
    """retourne le masque utilisé dans le QRcode

    Args:
        L (list): QRcode

    Returns:
        int: le masque utilisé dans le QRcode
    """
    iforma = informat.recupinformat(L) #on récupère les informations de format
    masq = 0
    for i in range(3): # on cherche le masque utilisé
        masq += iforma[2+i] *(10**(2-i))
    return masq

def retirer_masque(L:list, c:list) -> None:
    """retire le masque du QRcode

    Args:
        L (list): QRcode
        version (int): version du QRcode.
    """
    masque = masque_utilise(L)
    funcs = {0:mask_000, 1:mask_001, 10:mask_010, 11:mask_011, 100:mask_100, 101:mask_101, 110:mask_110, 111:mask_111}
    funcs.get(masque)(L, c)
    return L