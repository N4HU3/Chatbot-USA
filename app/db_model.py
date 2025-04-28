from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Interactions(db.Model):
    __tablename__ = 'Interactions'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    campaign = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Records(db.Model):
    __tablename__ = 'Records'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), nullable=False)
    campaign = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    number = db.Column(db.String(50), nullable=True)
    mail = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    operador = db.Column(db.String(100), nullable=True)
    checkTerminos = db.Column(db.String(50), nullable=True)
    habeastime = db.Column(db.DateTime, nullable=True)


class Survey(db.Model):
    __tablename__ = 'survey'

    id = db.Column(db.Integer, primary_key=True)
    guid = db.Column(db.String(36), nullable=False)
    rating1 = db.Column(db.Integer)
    rating2 = db.Column(db.Integer)
    campaign = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class DBModel:
    def __init__(self, app):
        db.init_app(app)
        with app.app_context():
            db.create_all()
