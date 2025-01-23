import structure as st
import fonctionsutiles as fu
import os
import csv

def utilisable(data:list)->list:
    data = data.split(", ")
    D = []
    for i in range(len(data)//2):
        temp = data[2*i]
        temp1 = data[2*i+1]
        D.append((int(temp[temp.count('(')+temp.count('['):]),int(temp1[:-(temp1.count(')')+temp1.count(']'))])))
    return D

def loc_alignements(v:int)->list:
    os.chdir("./image_test_QRcode/empirique")
    # Ouvrir le fichier CSV et le convertir en liste
    with open('loisempiriques.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        data_list = list(csvreader)
    data_list = utilisable(data_list[v][1])
    return  data_list

def construit(v:int)->list:
    QRcode = st.Gen_QRcode(21+4*(v-1))
    loc = loc_alignements(v)
    motif = st.alignment()
    for i in range(len(loc)):
        st.insert(QRcode,motif,(loc[i][0]-2,loc[i][1]-2))
    return QRcode

def main():
    Q = construit(37)
    fu.affiche_image(Q)

if __name__ == "__main__":
    main()