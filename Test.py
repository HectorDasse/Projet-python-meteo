import requests
from TinyDb import TinyDb

r = requests.get("http://app.objco.com:8099/?account=NTB37PKZUG&limit=5")

tab = r.json()

DataBase = TinyDb()
compteur = 1

for ligne in tab:
    DataBase.Add(compteur, TimeStamp = ligne[1], Valeur = ligne[0])
    compteur += 1
