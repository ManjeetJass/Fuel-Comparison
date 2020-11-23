import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    URL = 'http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?'
