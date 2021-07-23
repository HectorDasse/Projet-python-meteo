from tinydb import TinyDB, Query
from datetime import datetime

class base:

    db = None
    dbCapteur = None

    def __init__(self):
        self.db = TinyDB('db.json')
        self.dbCapteur = TinyDB('dbCapteur.json')

    def Trunc(self):
        self.db.truncate()

    def Add(self, idCapteur, TimeStamp, Temperature, Humidite, voltage):
        if self.rechercheDate(TimeStamp, idCapteur) is None:
            self.db.insert({"IDCapteur" : idCapteur, "Temperature" : Temperature, "Humidite" : Humidite, "TimeStamp" : TimeStamp, "Voltage" : voltage})

    def rechercheDate(self, TimeStampValeur, idCapteur):
        requete = Query()
        reponse = self.db.search((requete.IDCapteur == idCapteur) & (requete.TimeStamp == TimeStampValeur))
        if reponse != []:
            return reponse
        else:
            return None

    def GetAll(self):
        return self.db.all()

    def GetResults(self, nombreResult):
        tab = []
        for i in range (1, nombreResult):
            indice = i * -1
            tab.append(self.db.all()[indice])
        return tab

    def GetResultsGraph(self, idCapteur):
        tab = []
        requete = Query()
        reponse = self.db.search((requete.IDCapteur == idCapteur))
        for data in reponse:
            dateInput = data["TimeStamp"]
            dateInput = dateInput.replace(" GMT",'')
            dateOutput = datetime.strptime(dateInput, '%a, %d %b %Y %H:%M:%S') # détection du format initial
            dateOutput = dateOutput.strftime('%d/%m/%Y %H:%M:%S') # formatage de la date
            tab.append([data["Temperature"], dateOutput, data["Humidite"]])
        return tab

    def SaveCapteur(self, ID, Nom = "", minTemp = None, maxTemp = None, minHumidite = None, maxHumidite = None):
        requete = Query()
        reponse = self.dbCapteur.search((requete.IDCapteur == ID))
        if reponse != []:
            #update
            if Nom == "":
                return
            self.dbCapteur.update({'Nom': Nom, 'TemperatureMin' : minTemp, 'TemperatureMax' : maxTemp, 'HumiditeMin' : minHumidite, 'HumiditeMax' : maxHumidite}, requete.IDCapteur == ID)
        else:
            #add
            self.dbCapteur.insert({'IDCapteur': ID, 'Nom': Nom, 'TemperatureMin' : 0, 'TemperatureMax' : 0, 'HumiditeMin' : 0, 'HumiditeMax' : 0})



    def getCapteur(self):
        return self.dbCapteur.all()

    def getCapteurById(self, ID):
        requete = Query()
        return self.dbCapteur.search((requete.IDCapteur == ID))