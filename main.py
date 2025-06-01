import reedsolo as rs
import fonctionsbase as fb
import fonctionsutiles as fu
import mask as mk
import construction as co
import image_QRcode_to_liste as iQTL
import matplotlib.image as mpimg
# 1 = noir et 0 = blanc
"""
main.py
 ├──> construction.py
 │      ├──> structure.py
 │      ├──> fonctionsbase.py
 │      └──> informationsversion.py
 ├──> fonctionsutiles.py
 │      ├──> structure.py
 │      ├──> fonctionsbase.py
 │      ├──> mask.py
 │      └──> image_QRcode_to_liste.py
 ├──> mask.py
 """

def reedsolomon(bits:list, lvl : int) -> list:
    """Encode les données avec le code correcteur de Reed-Solomon

    Args:
        bits (list): données à encoder
        lvl (int): niveau de correction
    Returns:
        encoded_data (list): liste des données encodé
    """
    assert lvl in [25, 7, 30, 15]
    n = len(bits)
    donné = bytearray(bits) #on convertit les données en octets
    reeds = rs.RSCodec(int((0.02*lvl*n)//1+1))
    encoded_data = reeds.encode(donné)
    return [i for i in encoded_data]

def reedsolomon_decode(L:list, octets:list, lvl : int):
    pass

def encode_info(L:str, lvl:int) -> list:
    """Encode les informations dans un QRcode

    Args:
        L (str): information à encoder
        lvl (int): niveau de correction
    Returns:
        data (list): données encodées pas rs
    """
    assert lvl in [25, 7, 30, 15], "Niveau de correction invalide"
    type = fb.typeinfo(L)
    D = {"numérique":[0,0,0,1],"alphanumérique":[0,0,1,0],"kanji":[1,0,0,0],"binaire":[0,1,0,0]}
    data = D[type] #on ajoute le type d'information encodée
    if type == "binaire":
        donnees = [int(i) for i in L]
    else :
        donnees = fb.str_to_bits(L) #on convertit les données en bits avec la table Unicode
    data += fb.int_to_bits(len(donnees)//8) + donnees + [0,0,0,0] #on constitue les données à encoder
    data = fb.bitstolist(data) #on convertit les données en octets
    reed = reedsolomon(data, lvl) #on encode les données avec le code correcteur de Reed-Solomon
    data = fb.listtobits(reed) #on convertit les données en bits
    return data

def QRcode(S:str, lvl:int) -> list:
    """Encode les informations dans un QRcode

    Args:
        S (str): information à encoder
        lvl (int): niveau de correction
    Return:
        L (list): QRcode
    """
    data = encode_info(S, lvl) #on encode les informations dans un QRcode
    L, v = co.construit(data) #on construit la structure du QRcode
    cases = fu.cases_interdites(L, v) #on récupère les cases interdites du QRcode
    L = fu.ecriture(L, data, v, cases) #on écrit les données dans le QRcode
    mk.maskoptimal(L, lvl, cases) #on applique le masque optimal
    L = fu.negatif(L) #on inverse les couleurs du QRcode
    L = co.silence(L) #on ajoute une zone de silence autour du QRcode
    return L

def read_QR(L:str) -> str:
    """Lit les informations d'un QRcode

    Args:
        L (str): emplacement de l'image du QRcode
    Returns:
        data (str): informations lues
    """
    img = mpimg.imread(L).tolist() #on lit l'image du QRcode
    img = iQTL.recalibrage(img) #on recalibre l'image pour que chaques élément corresponde à un carré du QRcode
    data = fu.decode(img) #on décode les données du QRcode
    return data

def main():
    msg = "Le QRcode" #"hello world" #input("Que voulez vous encoder ? ")
    lvl = 7 #int(input("Quel niveau de correction ? "))
    code = QRcode(msg, lvl)
    fu.affiche_image(code)
    #print(reedsolomon(b"Le QRcode", lvl))
    dec = fu.decode(code)
    print("Données décodées : ", dec)
    #print(code == QRcode(dec,7))

if __name__ == "__main__":
    main()
