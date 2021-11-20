import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '27URHGTW7URHRY4RTU'