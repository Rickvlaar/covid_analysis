import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                            'covid_analysis.db')


class Endpoints(object):
    RIVM_CUMULATIVE = 'https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_cumulatief.json'


class FlaskConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    FLASK_APP = 'main.py'

    # Flask development settings
    FLASK_ENV = 'development'
    DEBUG = True


