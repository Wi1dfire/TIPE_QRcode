import structure as st
import fonctionsutiles as fu
import os
import csv
import fonctionsbase as fb
import informationsversion as iv

def utilisable(data:list)->list:
    """rend utilisable les données extraites d'un fichier csv similaire à : loisempiriques.csv

    Args:
        data (list): données extraites

    Returns:
        list: données rendu utilisable
    """
    data = data.split(", ")
    D = []
    for i in range(len(data)//2):
        temp = data[2*i]
        temp1 = data[2*i+1]
        D.append((int(temp[temp.count('(')+temp.count('['):]),int(temp1[:-(temp1.count(')')+temp1.count(']'))])))
    return D

def loc_alignements(v:int)->list:
    """renvoie la liste des localisations des motifs d'alignements pour une version de QRcode donnée

    Args:
        v (int): version

    Returns:
        list: liste des localisations des motifs d'alignements
    """
    dir = "image_test_QRcode\empirique"
    if dir != os.getcwd()[-len(dir):]:
        os.chdir("./image_test_QRcode/empirique")
    # Ouvrir le fichier CSV et le convertir en liste
    with open('loisempiriques.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        data_list = list(csvreader)
    data_list = utilisable(data_list[v][1])
    return  data_list

def construit(L:list)->tuple[list, int]:
    """construit le "squelette" du QRcode de la bonne version (qui sera renvoyée) 
    à partir des données que l'on veut y encoder

    Args:
        L (list): données que l'on veut encoder

    Returns:
        tuple[list, int]: squelette du QRcode et sa version
    """
    v = version(L)
    n = 21 + 4*(v-1)
    QRcode = st.Gen_QRcode(n)
    loc = loc_alignements(v)
    motif = st.alignment()
    for i in range(len(loc)):
        st.insert(QRcode,motif,(loc[i][0]-2,loc[i][1]-2))
    if v >= 7:
        vers = fb.int_to_bits(v)[2:]
        infovers = iv.informationsversion(vers)
        for i in range (len(infovers)):
            QRcode[i//3][n-11+(i%3)] = infovers[i]
            QRcode[n-11+(i%3)][i//3] = infovers[i]
    return QRcode, v

def version(L:list)->int:
    """détermine la version d'un QRcode
    à partir des données que l'on veut y encoder

    Args:
        L (list): données que l'on veut encoder

    Returns:
        int: version du QRcode necessaire
    """
    n = len(L)
    os.chdir(".\\image_test_QRcode\\empirique")
    # Ouvrir le fichier CSV et le convertir en liste
    with open('loisempiriques.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        data_list = list(csvreader)
    for i in range(1,41):
        if n <= int(data_list[i][3]):
            return i

def silence(L:list, larg:int = 4)->list:
    """Ajoute une zone de silence autour du QRcode

    Args:
        L (list): QRcode
        larg (int, optional): largeur de la zone de silence. Defaults to 4.

    Returns:
        list: QRcode avec une zone de silence
    """
    n = len(L)
    hb = [[1] * (n + 2 * larg) for _ in range(larg)]
    for i in range(n):
        L[i] = [1]*larg + L[i] + [1]*larg
    return hb + L + hb

def main():
    pass

if __name__ == "__main__":
    main()