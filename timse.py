#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app.controller import *

DataController(name="John Doe", address="Sesame Street 123",
               uri="https://doe-shop.com", email="john@doe-shop.com",
               data_protection_information="https://doe-shop.com/privacy")

DataProtectionOfficer(name="Jane Derpsen", email="jane@doe-shop.com")

startTimse()
