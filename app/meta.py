#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_restplus import fields
import datetime

from app.settings import *
from app.data_disclosed import *
from app.purpose import *
from app.legitimate_interest import *

class Meta(fields.Raw):
    def __init__(self, source=None):
        self.timse_version = TimseSettings.VERSION
        self.timestamp = str(datetime.datetime.now())
        self.source = source
        self.method = TimseSettings.INFO_PATH

    def get(self):
        return { "timse_version" : self.timse_version,
                 "timestamp" : self.timestamp,
                 "source" : self.source,
                 "method" : self.method }
