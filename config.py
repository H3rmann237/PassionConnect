import os

class Config:
    SECRET_KEY = 'bof'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///passionconnect.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False