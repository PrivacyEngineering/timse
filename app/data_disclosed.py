#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class DataDisclosed:
    # Identifying
    NAME                                 = 'Name'
    USERNAME                             = 'Username'
    UNIQUE_IDENTIFIER                    = 'Unique identifier'
    GOVERNMENT_ISSUED_IDENTIFICATION     = 'Government Issued Identification'
    PICTURE                              = 'Picture'
    BIOMETRIC_DATA                       = 'Biometric data'
    ADDRESS                              = 'Adress'
    PLACE_OF_BIRTH                       = 'Place of birth'
    DATA_OF_BIRTH                        = 'Data of birth'

    # Ethnicity
    RACE                                 = 'Race'
    NATIONAL_ORIGIN                      = 'National origin'
    LANGUAGE                             = 'Language'

    # Sexual
    GENDER_IDENTITY                      = 'Gender identity'
    PREFERENCES                          = 'Preferences'

    # Behavioural
    BROWSING_BEHAVIOUR                   = 'Browsing behaviour'
    CALL_LOGS                            = 'Call logs'
    LINKS_CLICKED                        = 'Links clicked'
    ATTITUDE                             = 'Attitude'

    # Demographic
    AGE_RANGES                           = 'Age ranges'
    PHYSICAL_TRAITS                      = 'Physcial traits'
    INCOME_BRACKETS                      = 'Income brackets'
    GEOGRAPHIC                           = 'Geographic'

    # Medical and Health
    PHYSICAL_HEALTH                      = 'Physcial health'
    MENTAL_HEALTH                        = 'Mental health'
    DISABILITIES                         = 'Disabilities'
    HEALTH_HISTORY                       = 'Health history'
    DNA_CODE                             = 'DNA code'
    BLOOD_TYPE                           = 'Blood type'
    PRESCRIPTIONS                        = 'Prescriptions'

    # Physical characterics
    HEIGHT                               = 'Height'
    WEIGHT                               = 'Weight'
    AGE                                  = 'Age'
    HAIR_COLOR                           = 'Hair color'
    SKIN_TONE                            = 'Skin tone'

    # Financial
    CREDIT_CARD_NUMBER                   = 'Credit card number'
    BANK_ACCOUNT                         = 'Bank account'
    CAR                                  = 'Car'
    HOUSE                                = 'House'
    PURCHASES                            = 'Purchases'
    SALES                                = 'Sales'
    CREDIT                               = 'Credit'
    INCOME                               = 'Income'
    LOAN_RECORDS                         = 'Loan Records'
    TRANSACTIONS                         = 'Transactions'
    TAXES                                = 'Taxes'
    PURCHASE_HABITS                      = 'Purchase habits'
    CREDIT_WORTHINESS                    = 'Credit worthiness'
    CREDIT_STANDING                      = 'Credit standings'
    CREDIT_CAPACITY                      = 'Credit capacity'

    # Professional
    JOB_TITLE                            = 'Job title'
    SALARY                               = 'Salary'
    WORK_HISTORY                         = 'Work history'
    SCHOOL                               = 'School'

    # Communication
    FRIENDS                              = 'Friends'
    CONNECTIONS                          = 'Connections'
    MEMBERSHIPS                          = 'Memberships'
    ASSOCIATIONS                         = 'Associations'
    SOCIAL_GRAPH                         = 'Social graph'
    TELEPHONE                            = 'Telephone'
    VOICE_MAIL                           = 'Voice mail'
    E_MAIL                               = 'E-mail'

    def OTHER(self, abbreviation, full_text):
        setattr(DataDisclosed, abbreviation, full_text)
        return full_text

DATA_DISCLOSED = DataDisclosed()

# Add your own custom types here...
DATA_DISCLOSED.OTHER('LOCATION', 'Location')
