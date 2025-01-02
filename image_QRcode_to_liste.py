import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import numpy as np

os.chdir('./image_test_QRcode')
QRcode = (mpimg.imread('Qr-2.png')).tolist()
QRcode_multic = (mpimg.imread('QRcode_coca.jpg')).tolist()

def distance(a,b):
    V = (np.array(a) - np.array(b))**2
    return np.sqrt((sum(V)))

def projecteur(a):
    pass

def coins_QRcode(image):
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
    HG, HD, BG = coins_QRcode(image)
    image = image[HG[0]:BG[0]+1]
    n = len(image)
    for i in range (n):
        h = image[i].copy()
        image[i] = h[HG[1]:HD[1]+1]
    return image

def simplifie(image):
    n, m = len(image), len(image[0])
    blanc, noir = [1.0,1.0,1.0], [0.0,0.0,0.0]
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
    for i in range(len(image)):
        if image[i][0] == 1 :
            return int(i/7)

def recalibrage(image):
    cal = calibre(image)
    L = []
    for i in range (len(image)//cal+1):
        ligne = []
        for j in range (len(image)//cal+1):
            ligne.append(image[i*cal][j*cal])
        L.append(ligne)
    return L

"""QRcode = retire_silence(QRcode)
QRcode = simplifie(QRcode)
QRcode = recalibrage(QRcode)
plt.imshow(QRcode, cmap='gray', clim=(0,1))
plt.show()"""
blanc, noir = [1.0,1.0,1.0], [0.0,0.0,0.0]
"""print(distance(blanc, noir))"""
