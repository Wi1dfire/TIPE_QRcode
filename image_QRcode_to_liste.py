import os
import numpy as np
import fonctionsutiles as fu
import matplotlib.image as mpimg

def distance(a,b):
    V = (np.array(a) - np.array(b))**2
    return np.sqrt((sum(V)))

def projecteur(a):
    pass

def coins_QRcode(image):
    """Repère les coins haut gauche, haut droit et bas gauche du QRcode (premier pixel blanc)
    Et retourne les coordonnées sous forme de tuple

    Args:
        image (list): image

    Returns:
        tuples: coordonnées des coins haut gauche, haut droit et bas gauche
    """
    HG, HD, BG = [(0,0),True], [(0,0),True], [(0,0),True]
    noir = [0.0,0.0,0.0,1.0] 
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

def retire_silence(image):
    """retire la zonne de silence autour du QRcode

    Args:
        image (list): image

    Returns:
        list: image sans la zone de silence
    """
    HG, HD, BG = coins_QRcode(image)
    image = image[HG[0]:BG[0]+1]
    n = len(image)
    for i in range (n):
        h = image[i].copy()
        image[i] = h[HG[1]:HD[1]+1]
    return image

def simplifie(image):
    """remplace les pixels noirs par des 0 et les pixels blancs par des 1

    Args:
        image (list): image

    Returns:
        list : image simplifiée pour utilisation des fonctions de lecture de données de QRcode
    """
    image = retire_silence(image)
    blanc, noir = [1.0,1.0,1.0], [0.0,0.0,0.0]
    n, m = len(image), len(image[0])
    L = []
    for i in range (n):
        ligne = []
        for j in range(m):
            if image[i][j][:3] == noir :
                ligne.append(0)
            if image[i][j][:3] == blanc :
                ligne.append(1)
        L.append(ligne)
    return L

def calibre(image):
    """Trouve le nombre de pixels d'un carré du QRcode

    Args:
        image (list): image simplifiée et sans zone de silence

    Returns:
        int : nombre de pixels d'un carré du QRcode
    """
    for i in range(len(image)):
        if image[i][0] == 1 :
            return int(i/7)

def recalibrage(image):
    """recalibre l'image pour que chaques élément corresponde à un carré du QRcode

    Args:
        image (list): image simplifiée et sans zone de silence

    Returns:
        list : image simplifiée et sans zone de silence recalibrée
    """
    if type(image[0][0]) != int:
        image = simplifie(image)
    cal = calibre(image)
    L = []
    for i in range (len(image)//cal+1):
        ligne = []
        for j in range (len(image)//cal+1):
            ligne.append(image[i*cal][j*cal])
        L.append(ligne)
    return L


def main():
    os.chdir('./image_test_QRcode')
    QRcode = (mpimg.imread('Qr-2.png')).tolist()
    QRcode = recalibrage(QRcode)
    fu.affiche_image(QRcode)
    blanc, noir = [1.0,1.0,1.0], [0.0,0.0,0.0]
    """print(distance(blanc, noir))"""

if __name__ == "__main__":
    main()