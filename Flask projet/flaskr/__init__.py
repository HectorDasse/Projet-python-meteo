import os
import requests
from flask import Flask, render_template
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

            # print(tempHexaTab)

            # convertion de l'hexadécimal
            if tempHexaTab[0] is not None and tempHexaTab[0] != '':
                for i in range (int(tempHexaTab[16])):
                    id = str(tempHexaTab[18][0+22*i:8+22*i])
                    status = str(tempHexaTab[18][8+22*i:10+22*i])
                    voltage = float(int(tempHexaTab[18][10+22*i:14+22*i], 16))
                    voltage /= 1000
                    voltageFinal = str(voltage) + "V"
                    temperatureStatus = int(tempHexaTab[18][14+22*i:16+22*i], 16)
                    if temperatureStatus == 0:
                        temperature = float(int(tempHexaTab[18][16+22*i:18+22*i], 16))
                        temperature /= 10
                    elif temperatureStatus == 1:
                        temperature = - float(int(tempHexaTab[18][16+22*i:18+22*i], 16))
                        temperature /= 10
                    elif temperatureStatus == 16 or temperatureStatus == 17:
                        temperature = 'invalid'
                    else:
                        temperature = 'invalid'
                    temperatureFinal = temperature if type(temperature) == "<class 'string'>" else str(temperature) + "C"
                    humidity = int(tempHexaTab[18][18+22*i:20+22*i], 16)
                    humidityFinal = str(humidity) + "%" if humidity < 255 else "0%"
                    rssi = - int(tempHexaTab[18][20+22*i:22+22*i], 16)
                    rssiFinal = str(rssi) + "dBm"

                    DataBase.Add(id, tempDate, temperatureFinal, humidityFinal)
                    tempTagsData = [id, status, voltageFinal, temperatureFinal, humidityFinal, rssiFinal]

        print("Boucle")

    sched = BackgroundScheduler(daemon=True)
    sched.add_job(sensor,'interval',seconds=10)
    sched.start()

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
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/trunc')
    def trunc():
        base.base().Trunc()
        return 'Trunc'

    @app.route('/test')
    def test():
        DataBase = base.base()
        result = DataBase.GetAll()
        return render_template("DonneeCapteur.html", DonneeListe=result)

    @app.route("/")
    def index():
        return render_template('index.html')

    return app