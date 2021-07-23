from tinydb import TinyDB, Query
from datetime import datetime

class base:

    db = None

    def __init__(self):
        self.db = TinyDB('db.json')

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
            dateOutput = datetime.datetime.strptime(dateInput, '%a, %d %b %Y %H:%M:%S') # détection du format initial
            dateOutput = dateOutput.strftime('%d/%m/%Y %H:%M:%S') # formatage de la date
            tab.append([data["Temperature"], dateOutput, data["Humidite"]])
        return tab
