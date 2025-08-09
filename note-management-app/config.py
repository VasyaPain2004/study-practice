import os

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'instance', 'db.sqlite')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False