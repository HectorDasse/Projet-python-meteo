from tinydb import TinyDB, Query


class TinyDb:

    db = None

    def __init__(self):
        self.db = TinyDB('db.json')

    def Trunc(self):
        self.db.truncate()

    def Add(self, Table, Valeur, Capteur):
        self.db.insert({'type' : Table, 'Valeur' : Valeur, 'Capteur' : Capteur})

