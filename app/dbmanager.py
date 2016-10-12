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
    pingList.append(PingtestServer.PingtestServer("https://www.youtube.com/", "youtube"))
    pingList.append(PingtestServer.PingtestServer("https://www.google.cl/", "google"))
    pingList.append(PingtestServer.PingtestServer("https://www.facebook.com/", "facebook"))
    pingList.append(PingtestServer.PingtestServer("http://www.biobiochile.cl/", "biobiochile"))
    pingList.append(PingtestServer.PingtestServer("http://www.lun.com/", "lun"))
    pingList.append(PingtestServer.PingtestServer("https://www.wikipedia.org/", "wikipedia"))
    pingList.append(PingtestServer.PingtestServer("https://www.live.com/", "live"))
    pingList.append(PingtestServer.PingtestServer("https://www.yahoo.com/", "yahoo"))
    pingList.append(PingtestServer.PingtestServer("http://www.bancoestado.cl/", "bancoestado"))
    pingList.append(PingtestServer.PingtestServer("http://www.mercadolibre.cl/", "mercadolibre"))
    pingList.append(PingtestServer.PingtestServer("http://www.taringa.net/", "taringa"))
    pingList.append(PingtestServer.PingtestServer("http://www.yapo.cl/", "yapo"))

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
