#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class LegitimateInterest:
    CONSENT                      = 'Consent'
    CONTRACT                     = 'Contract'
    LEGAL_OBLIGATION             = 'Legal obligation'
    VITAL_INTERESTS              = 'Vital interests'
    PUBLIC_TASK                  = 'Public task'

    def OTHER(self, abbreviation, full_text):
        setattr(LegitimateInterest, abbreviation, full_text)
        return full_text

LEGITIMATE_INTEREST = LegitimateInterest()

# Add your own custom legitmate interests  here...
# LEGITIMATE_INTEREST.OTHER('CHKSMTHG', 'Check something secret.')
