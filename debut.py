import matplotlib.pyplot as plt
import random as rd
# 0 = noir et 1 = blanc

def init(n:int):
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

def motif():
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

def alignment():
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

def rotation(L:list):
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

def insert(L:list,patern:list,A:tuple):
    """insert un paterne carré dans une plus grande liste de liste carré 
    dont le coins haut gauche se trouve aux coordonnées A dans L.
    En place mais le return permet une utilisation plus facile.

    Args:
        L (list): liste dans laquelle insérer le paterne
        patern (list): paterne à insérer
        A (tuple): emplacement du du coins haut droit du patern à inséré dans la liste

    Returns:
        list: la liste avec le patern inséré
    """
    for i in range (len(patern)):
        for j in range (len(patern[i])):
            L[A[0]+i][A[1]+j] = patern[i][j]
    return L

def Gen_QRcode(n:int,o:bool):
    """Génère un QRcode de taille n

    Args:
        n (int): taille du QRcode
        o (bool): définit si le QRcode est bien orienté

    Returns:
        list: QRcode généré
    """
    if n < 14 : 
        return False
    L = init(n)
    paterne = motif()
    insert(L,paterne,(0,0)) #HG
    rotation(paterne)
    insert(L,paterne,(0,n-8)) #HD
    rotation(paterne)
    rotation(paterne)
    insert(L, paterne,(n-8,0)) #BG
    for i in range (n-15):
        if i % 2 != 0 :
            L[8+i][6] = 1
            L[6][8+i] = 1
    if not o :
        for i in range(rd.randint(1,3)):
            rotation(L)
    return L

def positionnement(L:list):
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

def positionnement2(L:list):
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

def affiche(L:list):
    """Affiche un QRcode de manière convenable

    Args:
        L (list): QRcode à afficher
    """
    for i in range (len(L)):
        print(L[i])

def affiche_image(L):
    """affiche le QRcode comment une image dans un plot

    Args:
        L (list): QRcode à afficher sous forme de l'image
    """
    plt.imshow(L, cmap='gray', clim=(0,1))
    plt.show()

def loc_alignment(L:list):
    Loc_centre = []
    ref = alignment()
    for i in range (len(L)-5):
        B = (L[i:i+5]).copy()
        for j in range (len(L)-5):
            b = True
            for k in range (len(B)):
                if ref[k] != B[k][j:j+5]:
                    b = False
            if b:
                Loc_centre.append((i+3,j+3))
    return Loc_centre

def cases_interdites(L:list):
    """Trouve les emplacements à on ne peut pas placer de bits/d'informations

    Args:
        L (list): QRcode dans lequel on cherche les emplacements interdits

    Returns:
        list : liste des emplacements interdits
    """
    cases = []
    n = len(L)
    for i in range (8): #on protège les motifs de positionnement et les informations sur le mask et le code correcteur
        for j in range (8):
            cases.append((i,j))
            cases.append((i,n-1-j))
            cases.append((n-1-i,j))
        cases.append((8,i))
        cases.append((i,8))
        cases.append((8,n-1-i))
        cases.append((n-1-i,8))
    cases.append((8,8))
    for i in range (n-17): #on protège les motifs de calibrage
        cases.append((9+i,6))
        cases.append((6,9+i))
    alignement = loc_alignment(L)
    for i in alignement : #on protège les motifs d'alignement
        for j in range (5):
            for k in range(5):
                cases.append((i[0]-3+j,i[1]-3+k))
    return cases

def retour_octet(L:list):
    """retourne un liste (en place). En place

    Args:
        L (list): liste à retourner 
    """
    for i in range (len(L)//2):
        L[i],L[-1-i] = L[-1-i],L[i]

def lecture(L:list):
    """lit les données dans le QRcode et les retournes dans une liste de liste (liste d'octets)

    Args:
        L (list): QRcode dans duquel lire les donner

    Returns:
        list : liste des octets
    """
    cases = cases_interdites(L)
    n = len(L)-1
    Données = [] #liste qui vat contenir tous les octets
    octet = [] #octet que le vat remplir avant de l'ajouter a la liste donnée
    for i in range ((n//2)-3): #on pacoure le QRcode en colonne de 2 de largeur
        for j in range (n+1): #on parcoure tout les lignes
            if len(octet) == 8: # si on a un octet complet, on l'ajoute à la liste d'octets Données
                Données.append(octet)
                octet = []
            if i % 2 == 0 : #parcour les colonnes de droite à gauche si l'indice est paire, on parcoure de bas en haut
                if (n-j,n-2*i) not in cases : # on commence par le bit à droite, si l'emplacement n'est pas interdit,  on ajoute le bits à l'octet en court
                    octet.append(L[n-j][n-2*i])
                if len(octet) == 8: # si on a un octet complet, on l'ajoute à la liste d'octets Données
                    Données.append(octet)
                    octet = []
                if (n-j,n-(2*i+1)) not in cases : # puis même chose pour le bit de gauche
                    octet.append(L[n-j][n-(2*i+1)])
            else : #parcour les colonnes de droite à gauche si l'indice est impaire, on parcoure de haut en bas
                if (j,n-2*i) not in cases : # on commence par le bit à droite, si l'emplacement n'est pas interdit,  on ajoute le bits à l'octet en court
                    octet.append(L[j][n-2*i])
                if len(octet) == 8: # si on a un octet complet, on l'ajoute à la liste d'octets Données
                    Données.append(octet)
                    octet = []
                if (j,n-(2*i+1)) not in cases : # puis même chose pour le bit de gauche
                    octet.append(L[j][n-(2*i+1)])
    for i in range (3): # on traite les dernières colonnes à part à cause de la colonne de calibration
        for j in range (n+1):#on parcoure tout les lignes
            if len(octet) == 8: # si on a un octet complet, on l'ajoute à la liste d'octets Données
                Données.append(octet)
                octet = []
            if i % 2 == 1 : #parcour les colonnes de droite à gauche si l'indice est impaire, on parcoure de bas en haut
                if (n-j,5-2*i) not in cases : # on commence par le bit à droite, si l'emplacement n'est pas interdit,  on ajoute le bits à l'octet en court
                    octet.append(L[n-j][5-2*i])
                if len(octet) == 8: # si on a un octet complet, on l'ajoute à la liste d'octets Données
                    Données.append(octet)
                    octet = []
                if (n-j,5-(i*2+1)) not in cases : # puis même chose pour le bit de gauche
                    octet.append(L[n-j][5-(i*2+1)])
            else : #parcour les colonnes de droite à gauche si l'indice est paire, on parcoure de haut en bas
                if (j,5-2*i) not in cases : # on commence par le bit à droite, si l'emplacement n'est pas interdit,  on ajoute le bits à l'octet en court
                    octet.append(L[j][5-2*i])
                if len(octet) == 8: # si on a un octet complet, on l'ajoute à la liste d'octets Données
                    Données.append(octet)
                    octet = []
                if (j,5-(i*2+1)) not in cases : # puis même chose pour le bit de gauche
                    octet.append(L[j][5-(i*2+1)])
    if len(octet) == 8: # si on a un octet complet, on l'ajoute à la liste d'octets Données
        Données.append(octet)
        octet = []
    return Données

def octetstoliste(L:list):
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

def ecriture(L:list, Données:list):
    """écrit une liste de données en binaire dans un QRcode
    En place mais le return permet une utilisation plus facile.

    Args:
        L (list): QRcode dans lequel écrire les octets
        octets (list): liste de données en binaire

    Returns:
        list: QRcode
    """
    cases = cases_interdites(L) #on liste les emplacements interdits
    n = len(L)-1
    for i in range ((n//2)-3): #on pacoure le QRcode en colonne de 2 de largeur
        for j in range (n+1): #on parcoure tout les lignes
            if i % 2 == 0 : #parcour les colonnes de droite à gauche si l'indice est paire, on parcoure de bas en haut
                if (n-j,n-2*i) not in cases : # on commence par le bit à droite, si l'emplacement n'est pas interdit écrit dedans
                    if len(Données) == 0 : #si on a plus de Données à écrire on place un 0 par défaut
                        L[n-j][n-2*i] = 0
                    else : #sinon on place le premier bit qui vient dans la liste Données et on le retire
                        L[n-j][n-2*i] = Données[0]
                        del Données[0]
                if (n-j,n-(2*i+1)) not in cases : # puis même chose pour le bit de gauche
                    if len(Données) == 0 : #si on a plus de Données à écrire on place un 0 par défaut
                        L[n-j][n-(2*i+1)] = 0
                    else : #sinon on place le premier bit qui vient dans la liste Données et on le retire
                        L[n-j][n-(2*i+1)] = Données[0]
                        del Données[0]
            else : #parcour les colonnes de droite à gauche si l'indice est impaire, on parcoure de haut en bas
                if (j,n-2*i) not in cases : # on commence par le bit à droite, si l'emplacement n'est pas interdit écrit dedans
                    if len(Données) == 0 : #si on a plus de Données à écrire on place un 0 par défaut
                        L[j][n-2*i] = 0
                    else : #sinon on place le premier bit qui vient dans la liste Données et on le retire
                        L[j][n-2*i] = Données[0]
                        del Données[0]
                if (j,n-(2*i+1)) not in cases: # puis même chose pour le bit de gauche
                    if len(Données) == 0 : #si on a plus de Données à écrire on place un 0 par défaut
                        L[j][n-(2*i+1)] = 0
                    else : #sinon on place le premier bit qui vient dans la liste Données et on le retire
                        L[j][n-(2*i+1)] = Données[0]
                        del Données[0]
    for i in range(3): # on traite les dernières colonnes à part à cause de la colonne de calibration
        for j in range(n+1): #on parcoure tout les lignes
            if i % 2 == 1 : #parcour les colonnes de droite à gauche si l'indice est impaire, on parcoure de bas en haut
                if (n-j,5-2*i) not in cases : # on commence par le bit à droite, si l'emplacement n'est pas interdit écrit dedans
                    if len(Données) == 0 : #si on a plus de Données à écrire on place un 0 par défaut
                        L[n-j][5-2*i] = 0
                    else : #sinon on place le premier bit qui vient dans la liste Données et on le retire
                        L[n-j][5-2*i] = Données[0]
                        del Données[0]
                if (n-j,5-(i*2+1)) not in cases : # puis même chose pour le bit de gauche
                    if len(Données) == 0 : #si on a plus de Données à écrire on place un 0 par défaut
                        L[n-j][5-(i*2+1)] = 0
                    else : #sinon on place le premier bit qui vient dans la liste Données et on le retire
                        L[n-j][5-(i*2+1)] = Données[0]
                        del Données[0]
            else : #parcour les colonnes de droite à gauche si l'indice est paire, on parcoure de haut en bas
                if (j,5-2*i) not in cases : # on commence par le bit à droite, si l'emplacement n'est pas interdit écrit dedans
                    if len(Données) == 0 : #si on a plus de Données à écrire on place un 0 par défaut
                        L[j][5-2*i] = 0
                    else : #sinon on place le premier bit qui vient dans la liste Données et on le retire
                        L[j][5-2*i] = Données[0]
                        del Données[0]
                if (j,5-(i*2+1)) not in cases: # puis même chose pour le bit de gauche
                    if len(Données) == 0 : #si on a plus de Données à écrire on place un 0 par défaut
                        L[j][5-(i*2+1)] = 0
                    else : #sinon on place le premier bit qui vient dans la liste Données et on le retire
                        L[j][5-(i*2+1)] = Données[0]
                        del Données[0]
    return L

def mask_000(L, interdit):
    """applique le masque 000 au QRcode

    Args:
        L (_type_): QRcode
        interdit (_type_): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and j%3 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_001(L, interdit):
    """applique le masque 001 au QRcode

    Args:
        L (_type_): QRcode
        interdit (_type_): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and (i+j)%3 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_010(L, interdit):
    """applique le masque 010 au QRcode

    Args:
        L (_type_): QRcode
        interdit (_type_): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and (i+j)%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_011(L, interdit):
    """applique le masque 011 au QRcode

    Args:
        L (_type_): QRcode
        interdit (_type_): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and i%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_100(L, interdit):
    """applique le masque 100 au QRcode

    Args:
        L (_type_): QRcode
        interdit (_type_): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and ((i*j)%3+i*j)%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_101(L, interdit):
    """applique le masque 101 au QRcode

    Args:
        L (_type_): QRcode
        interdit (_type_): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and ((i*j)%3+i+j)%2 == 0 :
                L[i][j] = (L[i][j] + 1) % 2

def mask_110(L, interdit):
    """applique le masque 110 au QRcode

    Args:
        L (_type_): QRcode
        interdit (_type_): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and (i/2+j/3)%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def mask_111(L, interdit):
    """applique le masque 111 au QRcode

    Args:
        L (_type_): QRcode
        interdit (_type_): liste des emplacements interdits
    """
    for i in range(len(L)):
        for j in range(len(L)):
            if (i,j) not in interdit and (i*j)%3+(i*j)%2 == 0 :
                L[i][j] = (L[i][j]+1)%2

def appli_mask(L, mask, interdit):
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

def encode(L, octets, mask):
    """Encode les informations sous la forme d'une list de bits dans un QRcode

    Args:
        L (_type_): QRcode
        octets (_type_): informations à encoder dans le QRcode
        mask (_type_): masque voulut
    """
    ###L = Gen_QRcode(len(octets)//2,True) #TROUVER UNE FORMULE POUR LA TAILLE (ça serait pas mal)
    verboten = cases_interdites(L) #on liste les emplacements interdit
    ecriture(L,octets) #on écrit les données
    appli_mask(L, mask, verboten) #on applique le masque voulut
    mask = str(mask)
    for i in range(3): #on inscrit le masque utilisé
        L[8][2+i], L[-(2+i)][8] = int(mask[i]), int(mask[i])

def decode(L):
    """Décode les informations sous la forme octets dans un QRcode

    Args:
        L (_type_): GRcode à décoder

    Returns:
        _type_: données décodé sous la forme de liste d'octets (sous la forme de liste)
    """
    verboten = cases_interdites(L) #on liste les emplacements interdit
    mask=0 #on prépare le masque qui à été utilisé
    for i in range(3): # on cherche le masque utilisé
        mask += L[8][2+i] *(10**(2-i))
    appli_mask(L, mask, verboten) #on réapplique le masque pour retrouver les données initiales
    données = lecture(L) # on lit les données du QRcode
    return données

def main():
    L = Gen_QRcode(29,True)
    n=len(L)-1
    alignement = alignment()
    L = insert(L,alignement,(n-8,n-8))
    c = cases_interdites(L)
    #appli_mask(L, 101, c)
    K = []
    """
    for i in range(72):
        K.append([1,1,0,0,1,0,1,1])
    données = octetstoliste(K)
    encode(L,données,101)
    affiche_image(L)
    """
    """
    for i in range(72):
        K.append([18,17,16,15,14,13,12,11])
    données = octetstoliste(K)
    ecriture(L,données)
    plt.imshow(L, cmap='rainbow', clim=(0,20))
    plt.show()
    """

# print("Done importing")
if __name__ == "__main__":
    print("Executing main")
    main()

"""for i in range(72):
    K.append([1,1,0,0,1,0,1,1])
données = octetstoliste(K)
encode(L,données,101)
affiche_image(L)"""

"""
for i in range(72):
    K.append([18,17,16,15,14,13,12,11])
données = octetstoliste(K)
ecriture(L,données)
plt.imshow(L, cmap='rainbow', clim=(0,20))
plt.show()
"""