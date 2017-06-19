#!/usr/bin/env python


import os

from flask import Flask
from flask import request
from flask import make_response
import requests
import logging
import sys

# Flask app should start in global layout
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)




@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers['apikey'] == 'a3be1e29-8d95-474c-9ae8-faa88ade48b4':
        response = requests.get('http://noecommercews1098.cloudapp.net/api.ai/webhook.ashx', data = request.data)
        return response.text
    else:
        return 'foo'

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
