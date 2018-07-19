#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_restplus import fields
import datetime

from app.meta import Meta

from app.settings import *
from app.data_disclosed import *
from app.purpose import *
from app.legitimate_interest import *

class TransparencyInformation(fields.Raw):
    def __init__(self, data_exchanges=[]):
        self.meta = Meta(source='/')
        self.data_exchanges = None

    def __str__(self):
        return str(self.get())

    def get(self):
        return { "meta" : self.meta.get(),
                 "data_controller" : self.data_controller,
                 "data_protection_officer" : self.data_protection_officer,
                 "data_exchanges" : self.data_exchanges }
