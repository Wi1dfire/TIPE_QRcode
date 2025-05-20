import image_QRcode_to_liste as iQTL
import fonctionsutiles as fu
import fonctionsbase as fb
import qrcode as qr
import matplotlib.image as mpimg
import os
import csv

def base_de_Qrcode():
    """
    Crée une base de 40 QRcodes de version 1 à 40
    """
    os.chdir('./QRcode')
    for i in range(1,41):
        qrcode = qr.QRCode( version=i, error_correction=qr.constants.ERROR_CORRECT_L, box_size=1, border=0)
        img = qrcode.make_image(fill='black', back_color='white')
        img.save("qrcodeV"+str(i)+".png")

def alignements_empiriques(img:list)->list:
    """
    renvoie l'emplacement des alignements dans l'image

    Args:
        img (list): QRcode

    Returns:
        list: liste des emplacement des alignements
    """
    return fu.loc_alignment(img)

def espace_empirique(img:list, version: int)->int:
    """
    retourne nombre de cases utilisables dans le QRcode

    Args:
        img (list): QRcode

    Returns:
        int: nombre de cases utilisables
    """
    return len(img)**2 - len(fb.unique(fu.cases_interdites(img,version)))

def tocsv(data:list)->None:
    """créé un fichier csv avec les données

    Args:
        data (list): liste des données
    """
    with open('loisempiriques.csv', 'w', newline='') as file:
        writer = csv.writer(file,delimiter=';')
        writer.writerows(data)

def remove_files():
    """
    supprime les fichiers de la base de QRcodes
    """
    for i in range(1,41):
        os.remove("./QRcode/qrcodeV"+str(i)+".png")

def main():
    os.chdir('./image_test_QRcode/empirique') #on se place dans le bon répertoire
    if len(os.listdir("./QRcode")) != 40: #on vérifie si la base de QRcodes est complète
        base_de_Qrcode()
    data = [['versions','alignements','taille','espace']] #on initialise la liste des données
    for i in range(1,41): #on parcourt les QRcodes
        img = mpimg.imread("./QRcode/qrcodeV"+str(i)+".png").tolist() #on charge l'image
        img = iQTL.recalibrage(img) #on la recalibre pour la rendre exploitable par le programme
        data.append([i,alignements_empiriques(img),len(img), espace_empirique(img,i)])#on ajoute les données à la liste des données
    tocsv(data) #on convertie les données en csv
    if len(os.listdir("./QRcode")) == 40: #on vérifie si la base de QRcodes est complète pour la supprimer
        remove_files()

if __name__ == "__main__":
    main()