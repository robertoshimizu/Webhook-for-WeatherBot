# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 10:39:04 2019

@author: rober
"""

import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout

app = Flask(__name__)

@app.route('/webhook',methods=['POST'])
def webhook():
    req = request.get_json(silent = True, force = True)
    print(json.dumps(req, indent = 4))
    
    res = makeResponse(req)
    res = json.dumps(res, indent = 4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResponse(req):
    queryResult = req.get("queryResult")
    # format of json file generated by DialogFlow to request fulfillment
    parameters = queryResult.get("parameters")
    city = parameters.get("geo-city")
    date = parameters.get("date")
    
    # Query Openweather API
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=402a99fb3bd6fc79f1e1478b763092f5')
    json_object = r.json()
    weather=json_object['list']
    for i in range(0,30):
        condition = weather[i]['weather'][0]['description']
        break
    
    # Dialogflow will expect following fields from response
    # speech, displayText, source
    
    speech = "The forecast for "+ city +" on " +date+" is "+condition
    
    return {
    "fulfillment_text": speech,
    #"fulfillment_messages":speech,
    "source": "apiai-weather-webhook"        
    }
    
if __name__ == '__main__':
    port = int(os.getenv('PORT',5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port = port, host='0.0.0.0')