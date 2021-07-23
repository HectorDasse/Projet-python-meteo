from tinydb import TinyDB, Query


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
            tab.append([data["Temperature"], data["TimeStamp"], data["Humidite"]])
        return tab

    def SaveCapteur(self, ID, Nom):
        requete = Query()
        reponse = self.dbCapteur.search((requete.IDCapteur == ID))
        if reponse != []:
            #update
            if Nom == "":
                return
            self.dbCapteur.update({'Nom': Nom}, requete.IDCapteur == ID)
        else:
            #add
            self.dbCapteur.insert({'IDCapteur': ID, 'Nom': Nom})

    def getCapteur(self):
        return self.dbCapteur.all()