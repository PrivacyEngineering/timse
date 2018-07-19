#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, json, jsonify, request, render_template,  send_from_directory, Response
from flask_restplus import Api, Resource, fields, marshal, marshal_with, Model
import datetime
import inspect

from app.meta import Meta
from app.transparency_information import TransparencyInformation
from app.data_protection_officer import DataProtectionOfficer
from app.data_exchange import DataExchange
from app.data_controller import DataController

from app.settings import *
from app.data_disclosed import *
from app.purpose import *
from app.legitimate_interest import *

from app.timse_parser import scan_all_decorators
from app.timse_inspector import scan_all_missing

app = Flask(__name__)
api = Api(app, version=TimseSettings.VERSION, title='TIMSE - Transparency in Multi-Service Environments', description='A transparency enhancing technology (TET) motivated by the General Data Protection Regulation (GDPR).')


'''
@timse(third_party='Paypal Inc',
    data_disclosed=[timse.DATA_DISCLOSED.NAME, timse.DATA_DISCLOSED.KREDIT],
    purpose=[timse.PURPOSE.IDENTITY_CHECK],
    storage_period=[30, 'seconds'])

timse.DATA_DISCLOSED.add('KREDIT', 'Kreditkarteninformation')
'''

meta_model = api.model('Meta', {
	'timse-version':   fields.Float(required=True, description='Version of timse in use.'),
	'timestamp':       fields.String(required=True, description='Date and time of document generation.'),
	'source':          fields.String(required=True, description='URL endpoint by which the document was created.'),
	'method':          fields.String(required=True, description='HTTP method used.'),
	'error':           fields.Boolean(required=True, description='Defines if an error occurred.')
	})

data_controller_model = api.model('DataController', {
	'name':            fields.String(required=True, description='Name of data controller.'),
	'address':         fields.String(required=True, description='Address of data controller.'),
    'uri':             fields.String(required=True, description='URI of the data controller (usually the microservice basepath.'),
	'email':           fields.String(required=True, description='Email address of data controller.'),
	'data_protection_information': fields.String(required=True, description='URL where to find general data protection information.')
	})

data_protection_officer_model = api.model('DataProtectionOfficer', {
	'name':            fields.String(required=True, description='Name of Data Protection Officer.'),
	'email':           fields.String(required=True, description='Email of Data Protection Officer.')
	})

data_exchange_model = api.model('DataExchange', {
    'third_party':      fields.String(required=True, description='Name of third party refelects to country-specific offical name.'),
	'data_disclosed':   fields.List(fields.String, required=True, description='Data (variables) disclosed.'),
    'purpose':          fields.List(fields.String, required=True, description='Purposes for which the data is used.'),
	'storage_period':   fields.String(required=True, description='DateTime string of how long the data disclosed is going to be saved (timedelta in seconds, minutes, hours, days or weeks).')
    # TODO legitimate_interest is going to be neglected for now, but there are already examples defined in legitimate_interest.py
	})

#transparency_information_model = api.model('TransparencyInformation', {
#    'meta' : Meta(),
#    'data_controller' : DataController(),
#    'data_protection_officer' : DataProtectionOfficer(),
#    'data_exchanges' : fields.List(DataExchange(None, None, None, None), required=True)
#})

ns = api.namespace('x', description='Provides status information about the service.')
@ns.route('/status')
class Up(Resource):
    def get(self):
        return {'msg' : "timse started successfully!"}, 200

@ns.route('/meta')
class MetaPublic(Resource):
    #@ns.marshal_with(meta_model)
    def get(self):
        return Meta(source='/').get()

ns = api.namespace('Dashboard', description='Display the user interface')
@ns.route('/')
class Dashboard(Resource):
    def get(self):
        response = app.make_response(render_template(template_name_or_list='/visualization/index.html'))
        # print(response.headers)
        return response

@app.route('/json/<path:filename>')
@ns.param('filename', 'Path to json (e.g. test3.json) that can be loaded.')
def download_file(filename):
    return send_from_directory('templates/visualization',
                               filename, as_attachment=True)

ns = api.namespace('timse', description='timse Controller operations concerning providing transparency information.')



# transparency_information = TransparencyInformation()
# transparency_information.meta =
# print(transparency_information)
# print(DataExchange('hallo', 'something', PURPOSE.CHECK_IDENTITY, str(datetime.timedelta(seconds=2))).get())

@ns.route('/info')
@ns.param('path', 'Path to directory which should be scanned.')
class Info(Resource):
    #@ns.marshal_with(transparency_information_model)
    def get(self, path='test_case'):
        query_path = request.args.get('path', type=str)
        p = path if ((query_path is None) or (query_path == '')) else query_path

        transparency_information = TransparencyInformation()

        transparency_information.data_controller = DataController(
            DataController.name, DataController.address,
            DataController.uri, DataController.email,
            DataController.data_protection_information).get()

        transparency_information.data_protection_officer = DataProtectionOfficer(
            DataProtectionOfficer.name, DataProtectionOfficer.email).get()

        # Result pre-processing
        result = []
        for x in scan_all_decorators(p):
            print(x)
            third_party = x["third_party"]

            try:
                data_disclosed = getattr(DATA_DISCLOSED, x["data_disclosed"].split('.')[1])
            except:
                data_disclosed = "(?)"

            try:
                purpose = getattr(PURPOSE, x["purpose"].split('.')[1])
            except:
                purpose = "(?)"

            storage_period = x["storage_period"].replace(",", "").replace("'", "")

            result.append(DataExchange(third_party, data_disclosed, purpose, storage_period).get())
        transparency_information.data_exchanges = result

        return transparency_information.get()


@ns.route('/info-dashboard')
@ns.param('path', 'Path to directory which should be scanned (can be empty).')
class InfoDashboard(Resource):
    #@ns.marshal_with(transparency_information_model)
    def get(self, path='test_case'):
        query_path = request.args.get('path', type=str)
        p = path if ((query_path is None) or (query_path == '')) else query_path

        result = Info().get(p)
        dashboard = { "nodes" : [],
                      "edges" : [] }

        a = [ ({ "id" : x['third_party'],
                 "label" : x['third_party'],
                 "name" : "",
                 "address" : "",
                 "email" : "",
                 "data-protection-information" : ""
                 }) for x in result['data_exchanges'] ]

        list_of_unique_dicts = []
        for dict_ in a:
            if dict_ not in list_of_unique_dicts and not (dict_['id'] == ""): # TODO Do we really want to remove those?
                list_of_unique_dicts.append(dict_)

        dashboard['nodes'].extend(list_of_unique_dicts)
        dashboard['nodes'].append({
                 "id" : result['data_controller']['name'],
                 "label" : result['data_controller']['name'],
                 "name" : result['data_protection_officer']['name'],
                 "address" : result['data_controller']['address'],
                 "email" : result['data_protection_officer']['email'],
                 "data-protection-information" : result['data_controller']['data_protection_information']})

        id = 1
        for x in result['data_exchanges']:
            dashboard['edges'].append({
                "id" : id,
                "from" : result['data_controller']['name'],
                "to" : x['third_party'],
                "datadislosure" : x['data_disclosed'],
                "purpose" : x['purpose'],
                "period" : x['storage_period']
            })
            id = id + 1

        return dashboard


@ns.route('/inspector')
@ns.param('path', 'Path to directory which should be scanned (can be empty).')
class Inspector(Resource):
    def get(self, path='.'):
        query_path = request.args.get('path', type=str)
        p = path if ((query_path is None) or (query_path == '')) else query_path
        result = scan_all_missing(p)
        return result

@ns.route('/parser')
@ns.param('path', 'Path to directory which should be scanned (can be empty).')
class Inspector(Resource):
    def get(self, path='.'):
        query_path = request.args.get('path', type=str)
        p = path if ((query_path is None) or (query_path == '')) else query_path
        result = scan_all_decorators(p)
        return result

################################################################################
ns = api.namespace('static', description='timse Controller static categories.')
################################################################################

def get_static_info_by_class_name(name):
    all = [x for x in inspect.getmembers(name) if not x[0].startswith('__')]
    categories = [str(x[0]) for x in all]
    descriptions = [str(x[1]) for x in all]
    return dict(zip(categories, descriptions))

@ns.route('/data_disclosed')
class Data(Resource):
    def get(self):
        return get_static_info_by_class_name(DataDisclosed)

@ns.route('/purpose')
class Purp(Resource):
    def get(self):
        return get_static_info_by_class_name(Purpose)

@ns.route('/legitimate_interest')
class Legitimate(Resource):
    def get(self):
        return get_static_info_by_class_name(LegitimateInterest)

################################################################################
################################################################################
################################################################################

def test_static_information():
    print(LEGITIMATE_INTEREST.LEGAL_OBLIGATION)
    print(DATA_DISCLOSED.NAME)
    print(PURPOSE.CHECK_IDENTITY)
    print(LEGITIMATE_INTEREST.OTHER('HELLO', 'hello'))
    print(LEGITIMATE_INTEREST.HELLO)
    print(PURPOSE.OTHER('ELIAS', 'Elias'))
    print(DATA_DISCLOSED.OTHER('blub', 'blub'))

def startTimse():
    print('=== You successfully started TIMSE! Have fun. :-) ===')
    app.run(debug=True, host= '0.0.0.0', port=80)
