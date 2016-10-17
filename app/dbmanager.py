#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from app import app
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from Models import SpeedtestServer, PingtestServer

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adkDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'true'
db = SQLAlchemy(app)

def innitDB():
    db.create_all()
    setPingSites()
    print "Initiated DB OK"

def setPingSites():
    pingList = []
    pingList.append(PingtestServer.PingtestServer("YouTube", "https://www.youtube.com/"))
    pingList.append(PingtestServer.PingtestServer("Google", "https://www.google.cl/"))
    pingList.append(PingtestServer.PingtestServer("Facebook", "https://www.facebook.com/"))
    pingList.append(PingtestServer.PingtestServer("Radio BioBio Chile", "http://www.biobiochile.cl/"))
    pingList.append(PingtestServer.PingtestServer("Las Ultimas Noticias", "http://www.lun.com/"))
    pingList.append(PingtestServer.PingtestServer("Wikipedia", "https://www.wikipedia.org/"))
    pingList.append(PingtestServer.PingtestServer("Live", "https://www.live.com/"))
    pingList.append(PingtestServer.PingtestServer("Yahoo", "https://www.yahoo.com/"))
    pingList.append(PingtestServer.PingtestServer("Banco Estado", "http://www.bancoestado.cl/"))
    pingList.append(PingtestServer.PingtestServer("Mercadolibre", "http://www.mercadolibre.cl/"))
    pingList.append(PingtestServer.PingtestServer("Taringa", "http://www.taringa.net/"))
    pingList.append(PingtestServer.PingtestServer("Yapo", "http://www.yapo.cl/"))

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
