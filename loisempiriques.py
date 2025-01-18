import image_QRcode_to_liste as iQTL
import fonctionsutiles as fu
import qrcode as qr
import matplotlib.image as mpimg
import os
import csv

os.chdir('./image_test_QRcode/empirique/QRcode')

def base_de_Qrcode():
    for i in range(40):
        qrcode = qr.QRCode( version=i, error_correction=qr.constants.ERROR_CORRECT_L, box_size=10, border=0)
        img = qrcode.make_image(fill='black', back_color='white')
        img.save("qrcodeV"+str(i)+".png")

def alignements_empiriques():
    data = [["Version","liste des centres d'alignements"]]
    for i in range(40):
        img = mpimg.imread("qrcodeV"+str(i)+".png").tolist()
        img = iQTL.recalibrage(img)
        data.append([i, fu.loc_alignment(img)])
    with open('alignements.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def main():
    qrcode = qr.QRCode( version=1, error_correction=qr.constants.ERROR_CORRECT_L, box_size=1, border=0)
    img = qrcode.make_image(fill='black', back_color='white')
    img.save("qrcodeV"+str(1)+".png")
    image = mpimg.imread("qrcodeV"+str(1)+".png").tolist()
    image = iQTL.recalibrage(image)
    fu.affiche_image(image)
    fu.affiche(image)

if __name__ == "__main__":
    main()