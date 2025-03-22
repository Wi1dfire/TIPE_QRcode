import reedsolo as rs
import fonctionsbase as fb
import structure as st
import fonctionsutiles as fu
import mask as mk
import construction as co
# 0 = noir et 1 = blanc

def reedsolomon(bits:list, lvl : int) -> list:
    """(GC) Encode les données avec le code correcteur de Reed-Solomon

    Args:
        octets (list): données à encoder
        lvl (int): niveau de correction
    """
    n = len(bits)
    correction_symbols = int(n * lvl / 100)
    reeds = rs.RSCodec(correction_symbols)
    encoded_data = reeds.encode(bits)
    return encoded_data

def reedsolomon_decode(L:list, octets:list, lvl : int):
    pass

def typeinfo(L:str) -> str:
    """Retourne le type d'information

    Args:
        L (str): information

    Returns:
        str: type d'information
    """
    if all(c in '01' for c in L):
        return "binaire"
    if L.isnumeric():
        return "numérique"
    if L.isalnum():
        return "alphanumérique"
    return "kanji"

def encode_info(L:str, lvl:int) -> list:
    """Encode les informations dans un QRcode

    Args:
        L (str): information à encoder
        lvl (int): niveau de correction
    Returns:
        data (list): données encodées pas rs
    """
    assert lvl in [7, 15, 25, 30], "Niveau de correction invalide"
    type = typeinfo(L)
    D = {"numérique":[0,0,0,1],"alphanumérique":[0,0,1,0],"kanji":[1,0,0,0],"binaire":[0,1,0,0]}
    data = D[type] #on ajoute le type d'information encodée
    if type == "binaire":
        donnees = [int(i) for i in L]
    else :
        donnees = fb.str_to_bits(L) #on convertit les données en bits avec la table Unicode
    data += fb.int_to_bits(len(donnees)//8) + donnees + [0,0,0,0] #on constitue les données à encoder
    data = fb.bitstolist(data) #on convertit les données en octets
    reed = reedsolomon(data, lvl) #on encode les données avec le code correcteur de Reed-Solomon
    data += reed #on ajoute les données encodées par le code correcteur à la suite de celles déjà présentes
    data = fb.listtobits(data) #on convertit les données en bits
    return data

def inscritEC(L:list, lvl:int) -> list:
    """Inscrit les informations de correction d'erreur dans le QRcode

    Args:
        L (list): QRcode
        lvl (int): niveau de correction
    Returns:
        L (list): QRcode avec les informations de correction d'erreur inscrites
    """
    U = [7, 15, 25, 30]
    EC = bin(U.index(lvl))[2:]
    for i in range (len(EC)):
        L[8][i], L[-1-i][8] = int(EC[i]),int(EC[i])
    return L

def QRcode(S:str, lvl:int) -> list:
    """(GC) Encode les informations dans un QRcode

    Args:
        S (str): information à encoder
        lvl (int): niveau de correction
    """
    data = encode_info(S, lvl)
    L = co.construit(data)
    L = fu.ecriture(L, data)
    mk.maskoptimal(L)
    inscritEC(L, lvl)
    fu.affiche_image(L)
    return L

def main():
    msg = input("Que voulez vous encoder ? ")
    lvl = int(input("Quel niveau de correction ? "))
    code = QRcode(msg, lvl)
    print(fu.decode(code))
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

# print("Done importing")
if __name__ == "__main__":
    #print("Executing main")
    main()
