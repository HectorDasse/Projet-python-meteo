from tinydb import TinyDB, Query


class TinyDb:

    db = None

    def __init__(self):
        self.db = TinyDB('db.json')

    def Trunc(self):
        self.db.truncate()

    def Add(self, ID, Valeur, TimeStamp):
        self.db.insert({'ID' : ID, 'Valeur' : Valeur, 'TimeStamp' : TimeStamp})

    def rechercheDate(self, TimeStampValeur):
        rq = Query()
        if self.db.search(rq.TimeStamp == TimeStampValeur) != []:
            return None
        else:
            return self.db.search(rq.TimeStamp == TimeStampValeur)

