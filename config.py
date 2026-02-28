import os

class Config:
    SECRET_KEY = 'change-moi-plus-tard'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///passionconnect.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False