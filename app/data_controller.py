#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_restplus import fields
import datetime

from app.settings import *
from app.data_disclosed import *
from app.purpose import *
from app.legitimate_interest import *


class DataController(fields.Raw):
    def __init__(self, name=None, address=None, uri=None, email=None, data_protection_information=None):
        DataController.name = name
        DataController.address = address
        DataController.uri = uri
        DataController.email = email
        DataController.data_protection_information = data_protection_information

    def get(self):
        return { "name" : DataController.name,
                 "address" : DataController.address,
                 "uri" : DataController.uri,
                 "email" : DataController.email,
                 "data_protection_information" : DataController.data_protection_information }

    def format(self, value):
        return get(self)
