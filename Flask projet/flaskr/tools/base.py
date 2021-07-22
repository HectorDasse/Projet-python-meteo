from tinydb import TinyDB, Query


class base:

    db = None

    def __init__(self):
        self.db = TinyDB('db.json')

    def Trunc(self):
        self.db.truncate()

    def Add(self, idCapteur, TimeStamp, Temperature, Humidite):
        self.db.insert({'IDCapteur' : idCapteur, 'Temperature' : Temperature, 'Humidite' : Humidite, 'TimeStamp' : TimeStamp})

    def rechercheDate(self, TimeStampValeur, idCapteur):
        reponse = self.db.search(Query().fragment({'IDCapteur': idCapteur, 'TimeStamp': TimeStampValeur}))
        if reponse != []:
            return reponse
        else:
            return None

    def GetAll(self):
        tab = []
        for i in range (5):
            indice = i * -1
            tab.append(self.db.all()[indice])
        return tab