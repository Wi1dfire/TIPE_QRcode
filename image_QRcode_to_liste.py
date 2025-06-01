import numpy as np

def distance(a:list,b:list) -> int:
    """retourne la distance entre 2 points

    Args:
        a (list): point 1
        b (list): point 2

    Returns:
        _type_: _description_
    """
    V = (np.array(a) - np.array(b))**2
    return np.sqrt((sum(V)))

def projecteur(a):
    pass

def simplifie(image:list) -> list:
    """remplace les pixels noirs par des 0 et les pixels blancs par des 1

    Args:
        image (list): image

    Returns:
        list : image simplifiée pour utilisation des fonctions de lecture de données de QRcode
    """
    n, m = len(image), len(image[0])
    L = []
    if type(image[0][0]) == list:
        blanc, noir = [1.0,1.0,1.0], [0.0,0.0,0.0]
        for i in range (n):
            ligne = []
            for j in range(m):
                if image[i][j][:3] == noir :
                    ligne.append(0)
                if image[i][j][:3] == blanc :
                    ligne.append(1)
            L.append(ligne)
    if type(image[0][0]) == float:
        for i in range (n):
            ligne = []
            for j in range(m):
                ligne.append(int(image[i][j]))
            L.append(ligne)
    return L

def coins_QRcode(image:list) -> list:
    """Repère les coins haut gauche, haut droit et bas gauche du QRcode (premier pixel blanc)
    Et retourne les coordonnées sous forme de tuple

    Args:
        image (list): image

    Returns:
        tuples: coordonnées des coins haut gauche, haut droit et bas gauche
    """
    if type(image[0][0]) != int:
        image = simplifie(image)
    HG, HD, BG = [(0,0),True], [(0,0),True], [(0,0),True]
    noir = 0 
    n, m = len(image), len(image[0])
    for i in range ((n-1)//2):
        for j in range((m-1)//2):
            if image[i][j] == noir and HG[1]:
                HG = [(i,j), False]
            if image[i][-j] == noir and HD[1]:
                HD = [(i,m-1-j), False]
            if image[-i][j] == noir and BG[1]:
                BG = [(n-1-i,j), False]
    return HG[0], HD[0], BG[0],

def retire_silence(image:list) -> list:
    """retire la zonne de silence autour du QRcode

    Args:
        image (list): image

    Returns:
        list: image sans la zone de silence
    """
    HG, HD, BG = coins_QRcode(image)
    image = image[HG[0]:BG[0]+2]
    n = len(image)
    for i in range (n):
        h = image[i].copy()
        image[i] = h[HG[1]:HD[1]+2]
    return image

def calibre(image:list) -> int:
    """Trouve le nombre de pixels d'un carré du QRcode

    Args:
        image (list): image simplifiée et sans zone de silence

    Returns:
        int : nombre de pixels d'un carré du QRcode
    """
    for i in range(len(image)):
        if image[i][0] == 1 :
            return int(i/7)
    return 1

def recalibrage(image:list) -> list:
    """recalibre l'image pour que chaques élément corresponde à un carré du QRcode

    Args:
        image (list): image simplifiée et sans zone de silence

    Returns:
        list : image simplifiée et sans zone de silence recalibrée
    """
    if type(image[0][0]) != int:
        image = simplifie(image)
    image = retire_silence(image)
    cal = calibre(image)
    if cal == 1:
        return image
    L = []
    for i in range (len(image)//cal):
        ligne = []
        for j in range (len(image)//cal):
            ligne.append(image[i*cal][j*cal])
        L.append(ligne)
    return L


def main():
    print("executing main")

if __name__ == "__main__":
    main()