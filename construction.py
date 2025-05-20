import structure as st
import fonctionsutiles as fu
import os
import csv
import fonctionsbase as fb
import informationsversion as iv

def utilisable(data:list)->list:
    data = data.split(", ")
    D = []
    for i in range(len(data)//2):
        temp = data[2*i]
        temp1 = data[2*i+1]
        D.append((int(temp[temp.count('(')+temp.count('['):]),int(temp1[:-(temp1.count(')')+temp1.count(']'))])))
    return D

def loc_alignements(v:int)->list:
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
    n = len(L)
    qsdg = os.getcwd()
    os.chdir(".\\image_test_QRcode\\empirique")
    # Ouvrir le fichier CSV et le convertir en liste
    with open('loisempiriques.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        data_list = list(csvreader)
    for i in range(1,41):
        if n <= int(data_list[i][3]):
            return i


def main():
    pass

if __name__ == "__main__":
    main()