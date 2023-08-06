import os
import json
import threading
from requests import post, Session, Request
from flask import Flask, jsonify

AUTOREGISTER_MODE = 'AUTOREGISTER_MODE'
NORMAL_MODE = 'NORMAL_MODE'

CT_URL = os.getenv('CT_URL')
CT_TOKEN = os.getenv('CT_TOKEN')
API_VERSION = os.getenv('API_VERSION')

def autoregister(app, name, info, swagger, mode, ct_url=False, url=False, active=True):
    """Autoregister method"""
    payload = {'name': name, 'url': url, 'active': active}

    try:
        r = post(ct_url+'/api/v1/microservice', json=payload)
    except Exception as error:
        raise Exception('Generic error')

    if r.status_code != 200:
        raise ValueError('Microservice has not been registered')

def register(app, name, info, swagger, mode, ct_url=False, url=False, active=True):
    """Register method"""
    if mode == AUTOREGISTER_MODE:
        t = threading.Timer(5.0, autoregister, [app, name, info, swagger, mode, ct_url, url, active])
        t.start()

    @app.route('/info')
    def get_info():
        info['swagger'] = swagger
        return jsonify(info)

    @app.route('/ping')
    def get_ping():
        return 'pong'

def request_to_microservice(config, parse_json = True):
    """Request to microservice method"""
    try:
        session = Session()
        request = Request(
                method=config.get('method'),
                url=CT_URL + config.get('uri') if not API_VERSION else CT_URL + '/' + API_VERSION + config.get('uri'),
                headers={
                    'content-type': 'application/json',
                    'Authorization': 'Bearer '+CT_TOKEN
                },
                data=json.dumps(config.get('body'))
            )
        prepped = session.prepare_request(request)

        response = session.send(prepped)
    except Exception as error:
        raise error
    if parse_json == False:
        return response
    else:
        return response.json()
