import re
import matplotlib.pyplot as plt
import random as rd
import reedsolo as rs
import fonctionsbase as fb
import structure as st
import mask
# 0 = noir et 1 = blanc

def affiche(L:list) -> None:
    """Affiche un QRcode de manière convenable

    Args:
        L (list): QRcode à afficher
    """
    for i in range (len(L)):
        print(L[i])

def affiche_image(L) -> None:
    """affiche le QRcode comment une image dans un plot

    Args:
        L (list): QRcode à afficher sous forme de l'image
    """
    plt.imshow(L, cmap='gray', clim=(0,1))
    plt.show()

def loc_alignment(L:list) -> list:
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
                Loc_centre.append((i+3,j+3))
    return Loc_centre

def cases_interdites(L:list) -> list:
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
    for i in range (6): #on protège les zones contenant les informations sur la version
        for j in range (3):
            cases.append((i,n-11+j))
            cases.append((n-11+j,i))
    return cases

def lecture(L:list) -> list:
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

def ecriture(L:list, Données:list) -> list:
    """écrit une liste de données en binaire dans un QRcode
    En place mais le return permet une utilisation plus facile.

    Args:
        L (list): QRcode dans lequel écrire les octets
        Données (list): liste de données en binaire

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

def encode(L, octets, mask, lvl, type) -> None:
    """Encode les informations sous la forme d'une list de bits dans un QRcode

    Args:
        L (list): QRcode
        octets (list): informations à encoder dans le QRcode
        mask (int): masque voulut
    """
    ###L = Gen_QRcode(len(octets)//2,True) #TROUVER UNE FORMULE POUR LA TAILLE (ça serait pas mal)
    verboten = cases_interdites(L) #on liste les emplacements interdit
    ecriture(L,octets) #on écrit les données
    mask.appli(L, mask, verboten) #on applique le masque voulut
    mask = str(mask)
    for i in range(3): #on inscrit le masque utilisé
        L[8][2+i], L[-(2+i)][8] = int(mask[i]), int(mask[i])

def decode(L) -> list:
    """Décode les informations sous la forme octets dans un QRcode

    Args:
        L (list): QRcode à décoder

    Returns:
        list: données décodé sous la forme de liste d'octets (sous la forme de liste)
    """
    verboten = cases_interdites(L) #on liste les emplacements interdit
    mask=0 #on prépare le masque qui à été utilisé
    for i in range(3): # on cherche le masque utilisé
        mask += L[8][2+i] *(10**(2-i))
    mask.appli(L, mask, verboten) #on réapplique le masque pour retrouver les données initiales
    données = lecture(L) # on lit les données du QRcode
    return données

def reedsolomon(bits:list, lvl : int) -> list:
    """(GC) Encode les données avec le code correcteur de Reed-Solomon

    Args:
        octets (list): données à encoder
        lvl (int): niveau de correction
    """
    n = len(bits)
    correction_symbols = int(n * lvl / 100)
    reeds = rs.RSCodec(correction_symbols)
    encoded_data = reeds.encode(bits)
    return encoded_data

def reedsolomon_decode(L:list, octets:list, lvl : int):
    pass

def typeinfo(L:str) -> str:
    """Retourne le type d'information

    Args:
        L (str): information

    Returns:
        str: type d'information
    """
    if bool(re.search("^[0-9]*$", L)):
        return "numérique"
    if bool(re.search("^[A-Za-z0-9]*$", L)):
        return "alphanumérique"
    return "kanji"

def encode_info(L:str, lvl:int, type:str, version:int) -> list:
    """Encode les informations dans un QRcode

    Args:
        L (str): information à encoder
        lvl (int): niveau de correction
        type (str): type d'information
    Returns:
        data (list): données encodées pas rs
    """
    data = []
    if type == None: #On identifie le type d'information
        type = typeinfo(L)
    #On encode le type d'informations présente
    if type == "binaire":
        data = [0,1,0,0]
    if type == "numérique":
        data = [0,0,0,1]
    if type == "alphanumérique":
        data = [0,0,1,0]
    if type == "kanji":
        data = [1,0,0,0]
    donnees = fb.str_to_bits(L) #on convertit les données en bits avec la table Unicode
    data += fb.int_to_bits(len(donnees)//8) + donnees + [0,0,0,0] #on constitue les données à encoder
    data = fb.bitstooctet(data) #on convertit les données en octets
    reed = reedsolomon(data, lvl) #on encode les données avec le code correcteur de Reed-Solomon
    data += reed #on ajoute les données encodées par le code correcteur à la suite de celles déjà présentes
    return data

def main():
    L = st.Gen_QRcode(29,True)
    n=len(L)-1
    alignement = st.alignment()
    L = st.insert(L,alignement,(n-8,n-8))
    c = cases_interdites(L)
    #appli(L, 101, c)
    K = []
    """
    for i in range(72):
        K.append([1,1,0,0,1,0,1,1])
    données = octetstoliste(K)
    encode(L,données,101,None,None)
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
    """Helloworld_rs = encode_info("Hello World", 7, "alphanumérique", None)
    encode(L,Helloworld_rs,101,None,None)
    affiche_image(L)"""
    #print(len(reedsolomon([1,0,0,1,0,1,1,0], 7))%8)
    print(len(encode_info("Hello World", 7, "alphanumérique", None))%8)
    #print(len(fb.str_to_bits("Hello World"))//8)

# print("Done importing")
if __name__ == "__main__":
    #print("Executing main")
    main()
