import fonctionsutiles as fu
import evaluation as eval
import copy
import fonctionsbase as fb

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

def appli(L, mask, interdit) -> None:
    """applique le masque voulut au QRcode

    Args:
        L (list): Qrcode
        mask (int): masque souhaité
        interdit (list): liste des cases interdites à donner en argument à la fonction masque
    """
    funcs = {0:mask_000, 1:mask_001, 10:mask_010, 11:mask_011, 100:mask_100, 101:mask_101, 110:mask_110, 111:mask_111}
    funcs.get(mask)(L, interdit)
    masque = "00"+str(mask)
    masque = fb.strtolist(masque)[-3:]
    for i in range(3): #on inscrit le masque utilisé
        L[8][2+i], L[-(3+i)][8] = int(masque[i])-48, int(masque[i])-48

def choix_mask(L,c) -> int:
    """choisit le masque optimal pour le QRcode

    Args:
        L (list): QRcode
        interdit (list): liste des cases interdites

    Returns:
        int: masque optimal
    """
    score, mask = [], [0,1,10,11,100,101,110,111]
    for i in mask:
        test = copy.deepcopy(L)
        appli(test, i, c)
        score.append(eval.evaluer(test))
    return mask[score.index(min(score))]

def score(L,c) -> list:
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
        appli(test, i, c)
        score.append(eval.evaluer(test))
    return score, mask[score.index(min(score))]

def maskoptimal(L) -> None:
    """applique le masque optimal au QRcode

    Args:
        L (list): QRcode
    """
    c = fu.cases_interdites(L)
    return appli(L, choix_mask(L,c), c)

def retirer_masque(L) -> None:
    """retire le masque du QRcode

    Args:
        L (list): QRcode
    """
    masque = fu.masque_utilise(L)
    funcs = {0:mask_000, 1:mask_001, 10:mask_010, 11:mask_011, 100:mask_100, 101:mask_101, 110:mask_110, 111:mask_111}
    funcs.get(masque)(L, fu.cases_interdites(L))
    for i in range(3): #on retire le masque utilisé
        L[8][2+i], L[-(3+i)][8] = 0, 0
    return L