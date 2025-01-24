import image_QRcode_to_liste as iQTL
import fonctionsutiles as fu
import fonctionsbase as fb
import qrcode as qr
import matplotlib.image as mpimg
import os
import csv

def base_de_Qrcode():
    os.chdir('./QRcode')
    for i in range(1,41):
        qrcode = qr.QRCode( version=i, error_correction=qr.constants.ERROR_CORRECT_L, box_size=1, border=0)
        img = qrcode.make_image(fill='black', back_color='white')
        img.save("qrcodeV"+str(i)+".png")

def alignements_empiriques(img:list)->list:
    return fu.loc_alignment(img)

def espace_empirique(img:list)->list:
    return len(img)**2 - len(fb.unique(fu.cases_interdites(img)))

def tocsv(data:list)->None:
    with open('loisempiriques.csv', 'w', newline='') as file:
        writer = csv.writer(file,delimiter=';')
        writer.writerows(data)

def remove_files():
    for i in range(1,41):
        os.remove("./QRcode/qrcodeV"+str(i)+".png")

def main():
    os.chdir('./image_test_QRcode/empirique')
    if len(os.listdir("./QRcode")) != 40:
        base_de_Qrcode()
    data = [['versions','alignements','taille','espace']]
    for i in range(1,41):
        img = mpimg.imread("./QRcode/qrcodeV"+str(i)+".png").tolist()
        img = iQTL.recalibrage(img)
        data.append([i,alignements_empiriques(img),len(img), espace_empirique(img)])
    tocsv(data)
    if len(os.listdir("./QRcode")) == 40:
        remove_files()

if __name__ == "__main__":
    main()