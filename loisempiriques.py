import image_QRcode_to_liste as iQTL
import fonctionsutiles as fu
import qrcode as qr
import matplotlib.image as mpimg
import os
import csv

os.chdir('./image_test_QRcode/empirique')

def base_de_Qrcode():
    os.chdir('./QRcode')
    for i in range(1,41):
        qrcode = qr.QRCode( version=i, error_correction=qr.constants.ERROR_CORRECT_L, box_size=1, border=0)
        img = qrcode.make_image(fill='black', back_color='white')
        img.save("qrcodeV"+str(i)+".png")

def alignements_empiriques(img:list)->list:
    return fu.loc_alignment(img)

def tocsv(data:list)->None:
    with open('loisempiriques.csv', 'w', newline='') as file:
        writer = csv.writer(file,delimiter=';')
        writer.writerows(data)

def main():
    if len(os.listdir("./QRcode")) != 40:
        base_de_Qrcode()
    data = [['versions','alignements','taille']]
    for i in range(1,41):
        img = mpimg.imread("./QRcode/qrcodeV"+str(i)+".png").tolist()
        img = iQTL.recalibrage(img)
        data.append([i,alignements_empiriques(img),len(img)])
    tocsv(data)

if __name__ == "__main__":
    main()