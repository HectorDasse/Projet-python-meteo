from tinydb import TinyDB


class TinyDb:

    db = None

    def __init__(self):
        self.db = TinyDB('db.json')

    def Trunc(self):
        self.db.truncate()

    def Add(self, ID, Valeur, TimeStamp):
        self.db.insert({'ID' : ID, 'Valeur' : Valeur, 'TimeStamp' : TimeStamp})

