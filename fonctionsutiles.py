import structure as st
import mask
import fonctionsbase as fb
import matplotlib.pyplot as plt
import random as rd
import image_QRcode_to_liste as iql
import copy

rd.seed(0)

def negatif(L:list) -> list:
    """Effectue un négatif d'une liste de liste carrée.
    En place mais le return permet une utilisation plus facile.

    Args:
        L (list): liste qu'il faut négativer

    Returns:
        list: liste négativée
    """
    for i in range (len(L)):
        for j in range (len(L)):
            L[i][j] = 1 - L[i][j]
    return L

def affiche(L:list) -> None:
    """Affiche un QRcode de manière convenable

    Args:
        L (list): QRcode à afficher
    """
    for i in range (len(L)):
        print(L[i])

def affiche_image(L:list) -> None:
    """affiche le QRcode comment une image dans un plot

    Args:
        L (list): QRcode à afficher sous forme de l'image
    """
    plt.imshow(L, cmap='gray', clim=(0,1))
    plt.show()

def affiche_image_rainbow(L:list) -> None:
    """affiche le QRcode comment une image dans un plot avec un dégradé de couleur

    Args:
        L (list): QRcode à afficher sous forme de l'image
    """
    plt.imshow(L, cmap='rainbow')
    plt.show()

def loc_alignment(L:list) -> list:
    """localise les centres des motifs d'alignement dans un QRcode

    Args:
        L (list): QRcode dans lequel on cherche les motifs d'alignement

    Returns:
        list: liste des centres des motifs d'alignement
    """
    Loc_centre = []
    ref = st.alignment()
    for i in range (len(L)-5):
        B = (L[i:i+5]).copy()
        for j in range (len(L)-5):
            b = True
            for k in range (len(B)):
                if ref[k] != B[k][j:j+5]:
                    b = False
            if b:
                Loc_centre.append((i+2,j+2))
    return Loc_centre

def cases_interdites(L:list, version:int, format:bool = True) -> list:
    """Trouve les emplacements à on ne peut pas placer de bits/d'informations

    Args:
        L (list): QRcode dans lequel on cherche les emplacements interdits
        version (int): version du QRcode. Defaults to 0.
        format (bool, optional): si on veut protéger les informations de format. Defaults to True.

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
    if format: #on protège les informations de format
        for i in range (8):
            cases.append((i,8))
            cases.append((8,i))
            cases.append((8,n-1-i))
            cases.append((n-1-i,8))
        cases.append((8,8))
    for i in range (n-16): #on protège les motifs de calibrage
        cases.append((8+i,6))
        cases.append((6,8+i))
    alignement = loc_alignment(L)
    for i in alignement : #on protège les motifs d'alignement
        for j in range (5):
            for k in range(5):
                cases.append((i[0]-2+j,i[1]-2+k))
    if version >= 7: #on protège les informations de version
        for i in range (6): #on protège les zones contenant les informations sur la version
            for j in range (3):
                cases.append((i,n-11+j))
                cases.append((n-11+j,i))
    return cases

def lecture(L:list, version:int) -> list:
    """lit les données dans le QRcode et les retournes dans une liste de liste (liste d'octets)

    Args:
        L (list): QRcode dans duquel lire les donner
        version (int):version du QRcode

    Returns:
        list : liste des octets
    """
    cases = cases_interdites(L, version)
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

def ecriture(L:list, Données:list, version:int, cases:list =None) -> list:
    """écrit une liste de données en binaire dans un QRcode
    En place mais le return permet une utilisation plus facile.

    Args:
        L (list): QRcode dans lequel écrire les octets
        Données (list): liste de données en binaire
        version (int): version du QRcode
        cases (list, optional): liste des emplacements interdits. Defaults to None.

    Returns:
        list: QRcode
    """
    if cases is None: #si on ne donne pas de liste d'emplacements interdits, on les calcule
        cases = cases_interdites(L, version) #on liste les emplacements interdits
    n = len(L)-1
    for i in range ((n//2)-3): #on pacoure le QRcode en colonne de 2 de largeur
        for j in range (n+1): #on parcoure tout les lignes
            if i % 2 == 0 : #parcour les colonnes de droite à gauche si l'indice est paire, on parcoure de bas en haut
                if (n-j,n-2*i) not in cases : # on commence par le bit à droite, si l'emplacement n'est pas interdit écrit dedans
                    if len(Données) == 0 : #si on a plus de Données à écrire on place un 0 par défaut
                        L[n-j][n-2*i] = rd.randint(0,1)
                    else : #sinon on place le premier bit qui vient dans la liste Données et on le retire
                        L[n-j][n-2*i] = Données[0]
                        del Données[0]
                if (n-j,n-(2*i+1)) not in cases : # puis même chose pour le bit de gauche
                    if len(Données) == 0 : #si on a plus de Données à écrire on place un 0 par défaut
                        L[n-j][n-(2*i+1)] = rd.randint(0,1)
                    else : #sinon on place le premier bit qui vient dans la liste Données et on le retire
                        L[n-j][n-(2*i+1)] = Données[0]
                        del Données[0]
            else : #parcour les colonnes de droite à gauche si l'indice est impaire, on parcoure de haut en bas
                if (j,n-2*i) not in cases : # on commence par le bit à droite, si l'emplacement n'est pas interdit écrit dedans
                    if len(Données) == 0 : #si on a plus de Données à écrire on place un 0 par défaut
                        L[j][n-2*i] = rd.randint(0,1)
                    else : #sinon on place le premier bit qui vient dans la liste Données et on le retire
                        L[j][n-2*i] = Données[0]
                        del Données[0]
                if (j,n-(2*i+1)) not in cases: # puis même chose pour le bit de gauche
                    if len(Données) == 0 : #si on a plus de Données à écrire on place un 0 par défaut
                        L[j][n-(2*i+1)] = rd.randint(0,1)
                    else : #sinon on place le premier bit qui vient dans la liste Données et on le retire
                        L[j][n-(2*i+1)] = Données[0]
                        del Données[0]
    for i in range(3): # on traite les dernières colonnes à part à cause de la colonne de calibration
        for j in range(n+1): #on parcoure tout les lignes
            if i % 2 == 1 : #parcour les colonnes de droite à gauche si l'indice est impaire, on parcoure de bas en haut
                if (n-j,5-2*i) not in cases : # on commence par le bit à droite, si l'emplacement n'est pas interdit écrit dedans
                    if len(Données) == 0 : #si on a plus de Données à écrire on place un 0 par défaut
                        L[n-j][5-2*i] = rd.randint(0,1)
                    else : #sinon on place le premier bit qui vient dans la liste Données et on le retire
                        L[n-j][5-2*i] = Données[0]
                        del Données[0]
                if (n-j,5-(i*2+1)) not in cases : # puis même chose pour le bit de gauche
                    if len(Données) == 0 : #si on a plus de Données à écrire on place un 0 par défaut
                        L[n-j][5-(i*2+1)] = rd.randint(0,1)
                    else : #sinon on place le premier bit qui vient dans la liste Données et on le retire
                        L[n-j][5-(i*2+1)] = Données[0]
                        del Données[0]
            else : #parcour les colonnes de droite à gauche si l'indice est paire, on parcoure de haut en bas
                if (j,5-2*i) not in cases : # on commence par le bit à droite, si l'emplacement n'est pas interdit écrit dedans
                    if len(Données) == 0 : #si on a plus de Données à écrire on place un 0 par défaut
                        L[j][5-2*i] = rd.randint(0,1)
                    else : #sinon on place le premier bit qui vient dans la liste Données et on le retire
                        L[j][5-2*i] = Données[0]
                        del Données[0]
                if (j,5-(i*2+1)) not in cases: # puis même chose pour le bit de gauche
                    if len(Données) == 0 : #si on a plus de Données à écrire on place un 0 par défaut
                        L[j][5-(i*2+1)] = rd.randint(0,1)
                    else : #sinon on place le premier bit qui vient dans la liste Données et on le retire
                        L[j][5-(i*2+1)] = Données[0]
                        del Données[0]
    return L

def get_typeinfo(L:list) -> str:
    """retourne le type d'info encodée dans une liste de bits

    Args:
        L (list): liste de bits

    Returns:
        str: type d'information contenue
    """
    D = {(0,0,0,1):"numérique",(0,0,1,0):"alphanumérique",(1,0,0,0):"kanji",(0,1,0,0):"binaire"} #on définit les types d'informations
    for i in D.keys(): #on cherche le type d'information
        if all(L[x] == list(i)[x] for x in range(4)):
            return D[i] # on récupère le type d'information

def negatif(L:list, v:int =1) -> list:
    """rectifie le QRcode pour qu'il soit conforme aux normes

    Args:
        L (list): QRcode à rectifier
        v (int, optional): version du QRcode surtout utile pour les cases interdites. Defaults to 1.

    Returns:
        list: QRcode rectifié
    """
    n = len(L)
    interdit = cases_interdites(L, v, False) #on récupère les emplacements interdits
    for i in range(n):
        for j in range(n):
            if (i,j) not in interdit:
                L[i][j] = (L[i][j] + 1) % 2 #on inverse les bits qui ne sont pas interdits
    return L

def decode(QRcode:list) -> list:
    """Décode les informations sous la forme octets dans un QRcode

    Args:
        QRcode (list): QRcode à décoder

    Returns:
        list: données décodé sous la forme de liste d'octets (sous la forme de liste)
    """
    L = copy.deepcopy(QRcode) #on fait une copie de l'image pour ne pas la modifier
    L = iql.recalibrage(L) #on recalibre l'image
    L = negatif(L) #on inverse les bits pour retrouver les données initiales
    n = len(L) #on récupère la taille de l'image
    version = (n - 21)/4+1 #on récupère la version du QRcode
    c = cases_interdites(L, version) #on récupère les emplacements interdits
    mask.retirer_masque(L,c) #on retire le masque pour retrouver les données initiales
    données = fb.octetstoliste(lecture(L,version)) # on lit les données du QRcode
    tipe = get_typeinfo(données) #on récupère le type d'information
    données = données[4:] #on retire le type d'information
    length = fb.bitslisttoint(données[:8]) #on récupère la longueur de l'information
    données = données[8:8+length*8] #on garde que les données
    if tipe == "binaire":
        return "".join([str(i) for i in données]) #on retourne les données sous forme de chaine de caractère
    elif tipe == "numérique":
        return fb.bitstolist(données) #on retourne les données sous forme de liste d'octets
    else :
        return fb.bits_to_str(données) #on retourne les données sous forme de chaine de caractère

def main():
    print("Main function executed.")

if __name__ == "__main__":
    main()