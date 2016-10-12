#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.cors import CORS

app = Flask(__name__, static_url_path='/static')
CORS(app)

from app import views
