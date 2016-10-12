#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.dbmanager import db

class PingtestServer(db.Model):
    url = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name, url):
        super(PingtestServer, self).__init__()
        self.name = name
        self.url = url

    def __repr__(self):
        return '<%s>' % (self.url)

    def as_dict(self):
        return dict( (c.name, getattr(self, c.name)) for c in self.__table__.columns)
