from app.dbmanager import db

class SpeedtestServer(db.Model):
    url = db.Column(db.String(120), primary_key=True)
    added = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def __init__(self, url):
        super(SpeedtestServer, self).__init__()
        self.url = url

    def __repr__(self):
        return '<%s>' % (self.url)

    def as_dict(self):
        return dict( (c.name, getattr(self, c.name))
                     for c in self.__table__.columns)
