import os
import io
import requests
from flask import Flask, render_template, request
from .tools import base
from apscheduler.schedulers.background import BackgroundScheduler


def create_app(test_config=None):

    def sensor():
        r = requests.get("http://app.objco.com:8099/?account=NTB37PKZUG&limit=5")

        tab = r.json()

        DataBase = base.base()

        for ligne in tab:

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

            # convertion de l'hexadécimal
            if tempHexaTab[0] is not None and tempHexaTab[0] != '':
                payloadSize = int(tempHexaTab[17], 16) * 2
                for i in range (int(tempHexaTab[16])):
                    id = str(tempHexaTab[18][0+payloadSize*i:8+payloadSize*i])
                    status = str(tempHexaTab[18][8+payloadSize*i:10+payloadSize*i])
                    voltage = float(int(tempHexaTab[18][10+payloadSize*i:14+payloadSize*i], 16))
                    voltage /= 1000
                    voltageFinal = str(voltage) + "V"
                    temperatureStatus = int(tempHexaTab[18][14+payloadSize*i], 16)
                    if temperatureStatus == 0:
                        temperature = float(int(tempHexaTab[18][15+payloadSize*i:18+payloadSize*i], 16))
                        temperature /= 10
                    elif temperatureStatus == 4:
                        temperature = - float(int(tempHexaTab[18][15+payloadSize*i:18+payloadSize*i], 16))
                        temperature /= 10
                    else:
                        temperature = 'invalid'
                    temperatureFinal = temperature if type(temperature) == 'str' else str(temperature) + "C"
                    humidity = int(tempHexaTab[18][18+payloadSize*i:20+payloadSize*i], 16)
                    humidityFinal = str(humidity) + "%" if humidity == 255 else "0%"
                    rssi = - int(tempHexaTab[18][20+payloadSize*i:22+payloadSize*i], 16)
                    rssiFinal = str(rssi) + "dBm"

                    DataBase.SaveCapteur(id, "")
                    DataBase.Add(id, tempDate, temperatureFinal, humidityFinal, voltageFinal)
<<<<<<< HEAD
                    tempTagsData = [id, status, voltageFinal, temperatureFinal, humidityFinal, rssiFinal]
=======
                    #tempTagsData = [id, status, voltageFinal, temperatureFinal, humidityFinal, rssiFinal]
>>>>>>> 70f628d93ae8d2ebdf51c43bec158d749556e43e

        print("Boucle")

    """sched = BackgroundScheduler(daemon=True)
    sched.add_job(sensor,'interval',seconds=10)
    sched.start()"""

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/GetDonnee')
    def GetDonnee():
        sensor()
        return 'Hello, World!'

    @app.route('/trunc')
    def trunc():
        base.base().Trunc()
        return 'Trunc'

    @app.route('/Historique')
    def Historique():
        DataBase = base.base()
        result = DataBase.GetResults(11)
        return render_template("DonneeCapteur.html", DonneeListe=result)

    @app.route("/")
    def index():
        return render_template('index.html')



    colors = [
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

    @app.route('/GraphiqueTemperature', methods = ['POST'])
    def GraphiqueTemperature():
        labels = []
        values = []
        result = request.form
        id = result['ID']
        DataBase = base.base()
        tab = DataBase.GetResultsGraph(id)
        for data in tab:
            labels.append(data[1])
            temp = data[0]
            values.append(temp.replace("C", ""))

        bar_labels = labels
        bar_values = values
        return render_template('bar_chart.html', title='Capteur : ' + id, max=100, labels=bar_labels, values=bar_values, min = -50)

    @app.route('/GraphiqueHumidite', methods = ['POST'])
    def GraphiqueHumidite():
        labels = []
        values = []

        result = request.form
        id = result['ID']

        DataBase = base.base()
        tab = DataBase.GetResultsGraph(id)
        for data in tab:
            labels.append(data[1])
            temp = data[2]
            values.append(temp.replace("%", ""))

        bar_labels = labels
        bar_values = values
        return render_template('bar_chart.html', title='Capteur : ' + id, max=100, labels=bar_labels, values=bar_values, min = 0)

    @app.route('/saveCapteur', methods = ['POST'])
    def saveCapteur():
        result = request.form
        id = result['ID']
        nom = result['Nom']
        DataBase = base.base()
        DataBase.SaveCapteur(id, nom)

        return render_template('tabCapteur.html', CapteurListe = DataBase.getCapteur())

    @app.route("/capteur", methods= ["POST"])
    def capteur():
        result = request.form
        id = result['ID']
        nom = result['Nom']

        return render_template('Capteur.html', ID = id, Nom = nom)

    @app.route("/TabCapteur")
    def TabCapteur():
        DataBase = base.base()
        return render_template('tabCapteur.html', CapteurListe = DataBase.getCapteur())

    @app.route("/getTemp")
    def getTemp():
        ville = request.args.get('Ville')
        temp = 0
        if ville != None:
            url = "https://api.openweathermap.org/data/2.5/weather?q=" + ville + "&appid=acb39e08e1429f96311f0a99078ca8d2&units=metric"
            r = requests.get(url)

            tab = r.json()
            temp = tab["main"]["temp"]

        return render_template('Temperature.html', Ville = ville, Temp = temp)

    return app