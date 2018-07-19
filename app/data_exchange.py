#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_restplus import fields
import datetime

from app.settings import *
from app.data_disclosed import *
from app.purpose import *
from app.legitimate_interest import *

class DataExchange(fields.Raw):
    def __init__(self, third_party, data_disclosed, purpose, storage_period):
        self.third_party = third_party
        self.data_disclosed = data_disclosed
        self.purpose = purpose
        # self.legitimate_interest = legitimate_interest
        self.storage_period = storage_period

    def get(self):
        return { "third_party" : self.third_party,
                "data_disclosed" : self.data_disclosed,
                "purpose" : self.purpose,
                "storage_period" : self.storage_period }

                #print "seconds:", datetime.timedelta(seconds=1)
                #print "minutes:", datetime.timedelta(minutes=1)
                #print "hours:", datetime.timedelta(hours=1)
                #print "days:", datetime.timedelta(days=1)
                #print "weeks:", datetime.timedelta(weeks=1)
