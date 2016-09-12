import datetime
from app import app
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'true'
db = SQLAlchemy(app)

from Models import SpeedtestServer

def innitDB():
    db.create_all()
    print "OK"

def getActiveServers():
    sitios = SpeedtestServer.SpeedtestServer.query.all()
    return jsonify(data = [site.as_dict() for site in sitios])

def addActiveServer(request):
    url = request.base_url
    ip = request.environ['HTTP_HOST'].split(":")[0]
    port = request.environ['SERVER_PORT']
    sitio = SpeedtestServer.SpeedtestServer(ip,port,url)
    try:
        db.session.add(sitio)
        db.session.commit()
        return getActiveServers()
    except IntegrityError as e:
        return "ERROR %s" % e
