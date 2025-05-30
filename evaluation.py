import structure as st

def eval_line(L:list) -> int:
    """évalue une ligne du QRcode

    Args:
        L (list): QRcode

    Returns:
        int: score de ligne du QRcode
    """
    score = 0
    for i in L:
        n = 0
        p = i[0]
        for j in i:
            if j == p:
                n += 1
                if n == 5:
                    score += 3
                if n > 5:
                    score += 1
            else:
                n = 1
                p = j
    return score

def eval_col(L:list) -> int:
    return eval_line(st.rotation(L))

def eval_pixel(L:list) -> int:
    """évaluation du QRcode sur les pixel

    Args:
        L (list): QRcode

    Returns:
        int: score du QRcode sur les pixel
    """
    pixelnoir = 0
    for i in range(len(L)):
        pixelnoir += L[i].count(1)
    return abs(int((pixelnoir/len(L)**2)*100-50))*2

def eval_motif(L:list) -> int:
    """évaluation du QRcode sur les motifs

    Args:
        L (list): QRcode

    Returns:
        int: score du QRcode sur les motifs
    """
    motifs = [[0,1,0,0,0,1,0,1,1,1,1],[1,1,1,1,0,1,0,0,0,1,0],[1,1,1,1,0,1,0,0,0,1,0,1,1,1,1]]
    score = 0
    for i in L:
        for j in motifs:
            if j in i :
                score += 40
    M = L.copy()
    for i in st.rotation(M):
        for j in motifs:
            if j in i :
                score += 40
    return score

def eval_bloc(L:list) -> int:
    """évaluation du QRcode sur les blocs

    Args:
        L (list): QRcode

    Returns:
        int: score du QRcode sur les blocs
    """
    score = 0
    for i in range (len(L)-1):
        for j in range (len(L)-1):
            if L[i][j] == L[i+1][j] == L[i][j+1] == L[i+1][j+1] :
                score += 3
    return score

def evaluer(L:list) -> int:
    """évalue le QRcode

    Args:
        L (list): QRcode

    Returns:
        int: score du QRcode
    """
    return eval_pixel(L) + eval_line(L) + eval_col(L) + eval_motif(L) + eval_bloc(L)