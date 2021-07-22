import os

from flask import Flask, render_template
from .tools import base
from apscheduler.schedulers.background import BackgroundScheduler


def create_app(test_config=None):

    def sensor():
        """ Function for test purposes. """
        print("Scheduler is alive!")

    sched = BackgroundScheduler(daemon=True)
    sched.add_job(sensor,'interval',minutes=1)
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

    @app.route('/test')
    def test():
        DataBase = base.base()
        result = DataBase.GetAll()
        return render_template("DonneeCapteur.html", DonneeListe=result)

    @app.route("/")
    def index():
        return render_template('index.html')

    return app