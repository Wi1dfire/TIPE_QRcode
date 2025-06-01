import qrcode as qr
import os
import mask
import matplotlib.image as mpimg
import image_QRcode_to_liste as iQTL
import fonctionsutiles as fu  

os.chdir('./image_test_QRcode')
if "Le QRcode_V1L.png" not in os.listdir():
    qrcode = qr.QRCode(
        version=1,
        error_correction=qr.constants.ERROR_CORRECT_L,
        box_size=1,
        border=5,
        mask_pattern=5  # 101 en binaire = 5 en décimal
    )
    qrcode.add_data("LeQRcode")
    qrcode.make(fit=True)
    image = qrcode.make_image(fill='black', back_color='white')
    image.save("LeQRcode_V1L.png")
img = mpimg.imread("LeQRcode_V1L.png").tolist()
img = iQTL.recalibrage(img)
img = fu.negatif(img)
fu.affiche_image(img)
print(mask.masque_utilise(img))