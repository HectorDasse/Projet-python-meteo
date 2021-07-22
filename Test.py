import requests
from TinyDb import TinyDb

r = requests.get("http://app.objco.com:8099/?account=NTB37PKZUG&limit=5")

tab = r.json()

DataBase = TinyDb()
compteur = 1
tagsData = []
for ligne in tab:
    # ajout des données brutes en base
    # TODO ajout en base à revoir
    # DataBase.Add(compteur, TimeStamp = ligne[1], Valeur = ligne[0])
    tempId = ligne[0]
    tempHexa = ligne[1]
    tempDate = ligne[2]
    # segentation des données
    tempHexa = tempHexa.lower()
    tempHexaTab = [tempHexa[0:4], tempHexa[4:8], tempHexa[8:12], tempHexa[12:16], tempHexa[16:24], tempHexa[24:40],
                   tempHexa[40:52],
                   tempHexa[52:56],
                   tempHexa[56:60], tempHexa[60:62], tempHexa[62:64], tempHexa[64:68], tempHexa[68:72], tempHexa[72:76],
                   tempHexa[76:80], tempHexa[80:82], tempHexa[82:84], tempHexa[84:86], tempHexa[86:len(tempHexa)-12], # index 18 qui nous interesse
                   tempHexa[len(tempHexa)-12:len(tempHexa)-8], tempHexa[len(tempHexa)-8:len(tempHexa)-4], tempHexa[len(tempHexa)-4:len(tempHexa)]]

    print(tempHexaTab)

    # convertion de l'hexadécimal
    if tempHexaTab[0] is not None and tempHexaTab[0] != '':
        for i in range (int(tempHexaTab[16])):
            # TODO passer les int lignes 35,36 en float et ligne 38 en int signé
            tempTagsData = [tempHexaTab[18][0+22*i:8+22*i],
                            int(tempHexaTab[18][8+22*i:10+22*i], 16),
                            int(tempHexaTab[18][10+22*i:14+22*i], 16),
                            int(tempHexaTab[18][14+22*i:18+22*i], 16),
                            int(tempHexaTab[18][18+22*i:20+22*i], 16),
                            int(tempHexaTab[18][20+22*i:22+22*i], 16)]
            tagsData.append(tempTagsData)

    compteur += 1

# données de la charge utile
print(tagsData)