import reedsolo as rs
import fonctionsbase as fb
import structure as st
import fonctionsutiles as fu
import mask as mk
import construction as co
# 1 = noir et 0 = blanc

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
    L = fu.ecriture(L, data, v) #on écrit les données dans le QRcode
    mk.maskoptimal(L, lvl, v) #on applique le masque optimal
    L = fu.negatif(L) #on inverse les couleurs du QRcode
    L = co.silence(L) #on ajoute une zone de silence autour du QRcode
    return L

def main():
    msg = "Le QRcode" #"hello world" #input("Que voulez vous encoder ? ")
    lvl = 7 #int(input("Quel niveau de correction ? "))
    code = QRcode(msg, lvl)
    fu.affiche_image(code)
    #print(reedsolomon(b"Le QRcode", lvl))
    dec = fu.decode(code)
    print("Données décodées : ", dec)
    #print(code == QRcode(dec,7))
    """L = st.Gen_QRcode(29)
    n=len(L)-1
    alignement = st.alignment()
    L = st.insert(L,alignement,(n-8,n-8))
    c = fu.cases_interdites(L)
    K = []
    print(typeinfo("10012845640"))"""
    """
    for i in range(72):
        K.append([1,1,0,0,1,0,1,1])
    données = fb.octetstoliste(K)
    fu.encode(L,données,101,None,None)
    fu.affiche_image(L)
    """
    """
    for i in range(72):
        K.append([18,17,16,15,14,13,12,11])
    données = fb.octetstoliste(K)
    fu.ecriture(L,données)
    fu.affiche_image_rainbow(L)
    """

if __name__ == "__main__":
    main()
