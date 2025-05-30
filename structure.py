def rotation(L:list) -> list:
    """effectue une rotation de -pi/2 d'une liste de liste carrée.
    En place mais le return permet une utilisation plus facile. 

    Args:
        L (list): liste qu'il faut faire tourner 
    
    Returns :
        list : liste tourné de -pi/2
    """
    n = len(L)
    for i in range (n//2):
        for j in range(i,n-1-i):
            L[i][j],L[j][n-1-i]=L[j][n-1-i],L[i][j]
            L[n-1-j][i], L[i][j] = L[i][j], L[n-1-j][i]
            L[n-1-i][n-1-j], L[n-1-j][i] = L[n-1-j][i], L[n-1-i][n-1-j]
    return L

def init(n:int) -> list:
    """Créé un un tableau (liste de liste) de taille n*n remplit de 0

    Args:
        n (int): taille

    Returns:
        L (list): liste de liste de dimension n*n
    """
    L = []
    for i in range (n):
        L.append([0 for i in range (n)])
    return L

def motif() -> list:
    """Créé un motif de positionnement de référence

    Returns:
        list: motif de positionnement
    """
    L = init(8)
    for i in range (5):
        L[1][1+i] = 1
        L[1+i][5] = 1
        L[1+i][1] = 1
        L[5][1+i] = 1
    for i in range (8):
        L[7][i] = 1
        L[i][7] = 1
    return L

def alignment() -> list:
    """Créé un motif d'allignement de référence

    Returns:
        list: motif de d'allignement
    """
    L = init(5)
    for i in range (3):
        L[-2][i+1] = 1
        L[i+1][-2] = 1
        L[1][i+1] = 1
        L[i+1][1] = 1
    return L

def insert(L:list,patern:list,A:tuple) -> list:
    """insert un paterne carré dans une plus grande liste de liste carré 
    dont le coins haut gauche se trouve aux coordonnées A dans L.
    En place mais le return permet une utilisation plus facile.

    Args:
        L (list): liste dans laquelle insérer le paterne
        patern (list): paterne à insérer
        A (tuple): emplacement du du coins haut gauche du patern à inséré dans la liste

    Returns:
        list: la liste avec le patern inséré
    """
    for i in range (len(patern)):
        for j in range (len(patern[i])):
            L[A[0]+i][A[1]+j] = patern[i][j]
    return L

def positionnement(L:list) -> bool:
    """Vérifie si le QRcode est bien orienté

    Args:
        L (list): QRcode

    Returns:
        bool : si le QRcode est bien positionné
    """
    n = len(L)
    if n < 16 :
        return False
    paterne = motif()
    BG, HG, HD = [], [], []
    for i in range (8):
        HG.append(L[i][:8])
        BG.append(L[n-8+i][:8])
        HD.append(L[i][n-8:])
    rotation(BG)
    for i in range(3):
        rotation(HD)
    return HG == paterne and HD == paterne and  BG == paterne

def positionnement2(L:list) -> bool:
    """Vérifie si le QRcode est bien orienté

    Args:
        L (list): QRcode

    Returns:
        bool : si le QRcode est bien positionné
    """
    n = len(L)
    if n < 16 :
        return False
    paterne = motif()
    for i in range(8):
        for j in range (8):
            if L[i][j] != paterne[i][j] or L[n-8+i][j] != paterne[-i-1][j] or L[i][n-8+j] != paterne[i][-j-1]:
                return False
    return True