#!/usr/bin/env python
import os

from flask import Flask
from flask import request
from flask import make_response
import logging
import sys
from zeep import Client
from datetime import datetime
import json

# Flask app should start in global layout
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


@app.route('/webhook', methods=['POST'])
def webhook():
    chatresponse = {}
    try:
        #get the fulfilnment request
        fulfilmentrequest = request.data
        fulfilmentrequest = json.loads(fulfilmentrequest.decode('UTF-8'))
        client = Client('https://apiaiwebhookpassthough.herokuapp.com/static/content/EntitlementService.xml')    
        requesttype = client.get_element('ns2:EntitlementRequest')
        entitlementrequest = requesttype(BusinessOrgID = 1, ProductTypeCode = 'P', RequestedByUserID = '26may2017', SerialNumber = fulfilmentrequest['result']['parameters']['slno'], SymptomIDList = '0707')
        response = client.service.Entitle(request = entitlementrequest)
        warrantyexpirydate = response['Entitlement']['WarrantyExpiryDate']   
        if datetime.now() < warrantyexpirydate:
            chatresponse['displayText'] = "The phone is under warranty"
            chatresponse['speech'] = "Your phone is under warranty"
        else:
            chatresponse['displayText'] = "The phone is not under warranty"
            chatresponse['speech'] = "Your phone is not under warranty"
    except:
        chatresponse['displayText'] = "Unable to find warranty details!  Please check the serial number and try again"
        chatresponse['speech'] = "Check the serial number and try again"

    return json.dumps(chatresponse)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
