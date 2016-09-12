from app.dbmanager import db

class SpeedtestServer(db.Model):
    ip_address = db.Column(db.String(15), primary_key=True)
    port_address = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100), primary_key=True)
    added = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def __init__(self, ip,port,url):
        super(SpeedtestServer, self).__init__()
        self.ip_address = ip
        self.port_address = port
        self.url = url

    def __repr__(self):
        return '<%s (%s:%s)>' % (self.url,self.ip_address,self.port_address)

    def as_dict(self):
        return dict( (c.name, getattr(self, c.name))
                     for c in self.__table__.columns)
