import datetime
from app import app
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adkDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'true'
db = SQLAlchemy(app)

from Models import SpeedtestServer, PingtestServer

def innitDB():
    db.create_all()
    setPingSites()
    print "Initiated DB OK"

def setPingSites():
    pingList = []
    pingList.append(PingtestServer.PingtestServer("Google", "https://www.google.com"))
    pingList.append(PingtestServer.PingtestServer("Facebook", "https://www.facebook.com"))
    pingList.append(PingtestServer.PingtestServer("Universidad de Chile", "https://www.uchile.cl"))
    pingList.append(PingtestServer.PingtestServer("Yapo", "https://www.yapo.cl"))

    for pingSite in pingList:
        try:
            db.session.add(pingSite)
            db.session.commit()
            print "added %s " % pingSite
        except IntegrityError as e:
            db.session.rollback()

def getPingSites():
    sitios = PingtestServer.PingtestServer.query.all()
    return jsonify(data = [site.as_dict() for site in sitios])

def getActiveServers():
    sitios = SpeedtestServer.SpeedtestServer.query.all()
    return jsonify(data = [site.as_dict() for site in sitios])

def addActiveServer(request):
    url = request.headers['Referer']
    sitio = SpeedtestServer.SpeedtestServer(url)
    try:
        db.session.add(sitio)
        db.session.commit()
        print "addActiveServer OK"
    except IntegrityError as e:
        print "addActiveServer ERROR %s" % e
        db.session.rollback()
    return getActiveServers()
