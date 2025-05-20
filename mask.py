import fonctionsutiles as fu
import evaluation as eval
import copy
import fonctionsbase as fb
import informationsformat as informat

def mask_000(L, interdit) -> None:
    """applique le masque 000 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and (i+j)%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_001(L, interdit) -> None:
    """applique le masque 001 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and i%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_010(L, interdit) -> None:
    """applique le masque 010 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and j%3 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_011(L, interdit) -> None:
    """applique le masque 011 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and (i+j)%3 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_100(L, interdit) -> None:
    """applique le masque 100 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and (i/2+j/3)%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_101(L, interdit) -> None:
    """applique le masque 101 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and (i*j)%3+(i*j)%2 == 0 :
                L[i][j] = (L[i][j] + 1) % 2

def mask_110(L, interdit) -> None:
    """applique le masque 100 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and ((i*j)%3+i*j)%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_111(L, interdit) -> None:
    """applique le masque 111 au QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and ((i*j)%3+i+j)%2 == 0 :
                L[i][j] = (L[i][j] + 1) % 2

def appli(L, mask, interdit, cor) -> None:
    """applique le masque voulut au QRcode

    Args:
        L (list): Qrcode
        mask (int): masque souhaité
        interdit (list): liste des cases interdites à donner en argument à la fonction masque
    """
    funcs = {0:mask_000, 1:mask_001, 10:mask_010, 11:mask_011, 100:mask_100, 101:mask_101, 110:mask_110, 111:mask_111}
    funcs.get(mask)(L, interdit)
    masque = fb.strbtolistb(("00"+str(mask))[-3:])
    info = informat.informationsformat(cor, masque)
    #on inscrit les informations de format
    for i in range (8): 
        L[i][8], L[8][-1-i] = int(info[-1-i]), int(info[-1-i])
    for i in range (8, len(info)):
        L[8][7+8-i], L[-7+i-8][8] = int(info[-1-i]), int(info[-1-i])

def choix_mask(L,c,cor) -> int:
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
        appli(test, i, c, cor)
        score.append(eval.evaluer(test))
    return mask[score.index(min(score))]

def score(L,c,cor) -> list:
    """retourne le score de chaque masque

    Args:
        L (list): QRcode
        c (list): liste des cases interdites

    Returns:
        list: score de chaque masque
    """
    score, mask = [], [0,1,10,11,100,101,110,111]
    for i in mask:
        test = copy.deepcopy(L)
        appli(test, i, c,cor)
        score.append(eval.evaluer(test))
    return score, mask[score.index(min(score))]

def maskoptimal(L, lvl, version:int) -> None:
    """applique le masque optimal au QRcode

    Args:
        L (list): QRcode
        lvl (int): niveau de correction
        version (int): version du QRcode.
    """
    U = [7, 15, 25, 30]
    cor = fb.strbtolistb(bin(U.index(lvl))[2:])
    cor = [0]*(2-len(cor)) + cor
    c = fu.cases_interdites(L, version)
    return appli(L, choix_mask(L,c,cor), c, cor)

def retirer_masque(L, version:int) -> None:
    """retire le masque du QRcode

    Args:
        L (list): QRcode
        version (int): version du QRcode.
    """
    masque = fu.masque_utilise(L)
    funcs = {0:mask_000, 1:mask_001, 10:mask_010, 11:mask_011, 100:mask_100, 101:mask_101, 110:mask_110, 111:mask_111}
    funcs.get(masque)(L, fu.cases_interdites(L, version))
    return L