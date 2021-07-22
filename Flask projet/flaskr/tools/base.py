from tinydb import TinyDB, Query


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
        """

         tab = []
        for i in range (1, 6):
            indice = i * -1
            tab.append(self.db.all()[indice])
        return tab
        """
        return self.db.all()

