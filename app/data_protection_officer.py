#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_restplus import fields
import datetime

from app.settings import *
from app.data_disclosed import *
from app.purpose import *
from app.legitimate_interest import *

class DataProtectionOfficer(fields.Raw):
    def __init__(self, name=None, email=None):
        DataProtectionOfficer.name = name
        DataProtectionOfficer.email = email

    def get(self):
        return { "name" : DataProtectionOfficer.name,
                 "email" : DataProtectionOfficer.email }
