#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Purpose:
    CHECK_IDENTITY              = 'Check identity'
    CHECK_CREDITWORTHINESS      = 'Check Creditwothiness'
    CHECK_HEALTH_STATUS         = 'Check health status'
    CHECK_INTEGRITY             = 'Check integrity'

    def OTHER(self, abbreviation, full_text):
        setattr(PURPOSE, abbreviation, full_text)
        return full_text

PURPOSE = Purpose()

# Add your own custom purposes here...
PURPOSE.OTHER('CHKSMTHG', 'Check something secret.')
