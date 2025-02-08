import json
from venv import logger

from flask import app, request
import threading

@app.route('/notifications', methods=['POST'])
def ml_notifications():
    data = json.loads(request.data)

    try:
        # handle_meli_notification(data, app) 
        return json.dumps({'Sucesso!': True}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        print(f'Error in ML webhook: {e}')
        logger.error(f'[ML WEBHOOK ERROR] Text: {e}')
        return json.dumps({'Algo deu errado.': True}), 500, {'ContentType': 'application/json'}