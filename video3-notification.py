import json
import threading
from venv import logger

from flask import app, request

@app.route('/notifications', methods=['POST'])
def ml_notifications():
    data = json.loads(request.data)

    try:
        handle_meli_notification(data, app) # Implementar conforme regras de negócio
        
        # threading.Thread(target=handle_meli_notification,
        #                  args=(data, app,)).start()
        return json.dumps({'Sucesso!': True}), 200, {'ContentType': 'application/json'}
    except Exception as e:
        print(f'Error in ML webhook: {e}')
        logger.error(f'[ML WEBHOOK ERROR] Text: {e}')
        return json.dumps({'Algo deu errado.': True}), 500, {'ContentType': 'application/json'}Q