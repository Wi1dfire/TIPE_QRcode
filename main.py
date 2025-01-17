import reedsolo as rs
import fonctionsbase as fb
import structure as st
import fonctionsutiles as fu
import mask as mk
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
        type (str): type d'information
    Returns:
        data (list): données encodées pas rs
    """
    data = []
    type = typeinfo(L)
    #On encode le type d'informations présente
    if type == "numérique":
        data = [0,0,0,1]
    if type == "alphanumérique":
        data = [0,0,1,0]
    if type == "kanji":
        data = [1,0,0,0]
    if type == "binaire":
        data = [0,1,0,0]
        donnees = [int(i) for i in L]
    else :
        donnees = fb.str_to_bits(L) #on convertit les données en bits avec la table Unicode
    data += fb.int_to_bits(len(donnees)//8) + donnees + [0,0,0,0] #on constitue les données à encoder
    data = fb.bitstolist(data) #on convertit les données en octets
    reed = reedsolomon(data, lvl) #on encode les données avec le code correcteur de Reed-Solomon
    data += reed #on ajoute les données encodées par le code correcteur à la suite de celles déjà présentes
    data = fb.listtobits(data) #on convertit les données en bits
    return data

def main():
    L = st.Gen_QRcode(29,True)
    n=len(L)-1
    alignement = st.alignment()
    L = st.insert(L,alignement,(n-8,n-8))
    c = fu.cases_interdites(L)
    #mk.appli(L, 101, c)
    K = []
    print(typeinfo("10012845640"))
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
    fu.affiche_image(L)
    """
    """Helloworld_rs = encode_info("Hello World", 7, "alphanumérique", None)
    fu.encode(L,Helloworld_rs,101,None,None)
    fu.affiche_image(L)"""
    #print(len(reedsolomon([1,0,0,1,0,1,1,0], 7))%8)
    #print(len(encode_info("Hello World", 7))%8)
    #print(len(fb.str_to_bits("Hello World"))//8)

# print("Done importing")
if __name__ == "__main__":
    #print("Executing main")
    main()
