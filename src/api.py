from flask import Flask, request
from flask_cors import CORS
import json
import requests as rq

app = Flask(__name__)
CORS(app)

LOGS_PATH = 'logs/'
URL = 'http://ip-api.com/json/{}'
host = '127.0.0.1'
port = 8888

def maps(data):
    info = []
    src = [x for x in data if x != "0"]
    locations = []
    ips = []
    for ip in src:
        if ip not in ips:
            req = rq.get(URL.format(ip))
            try:
                jsonData = req.json()
                if jsonData['status'] == "success":
                    region = jsonData['city'] + ' - ' + jsonData['regionName'] + ', ' + jsonData['country'] + ', ' + jsonData['countryCode']
                    coords = [jsonData['lat'], jsonData['lon']]
                    if region not in locations:
                        info.append([region, coords, jsonData['isp']])
                        locations.append(region)
                        ips.append(ip)
            except:
                continue
    return json.dumps({'success': 1, 'result': info})


@app.route('/api', methods=['GET'])
def Api():
    req = request.args
    with open(LOGS_PATH + 'logs.csv', 'rt') as rt:
        read = rt.read().split('\n')
        rt.close()

    ndata = [x.split(',') for x in read]

    try:
        qnt = int(req['qnt'])
    except IndexError:
        qnt = 50

    try:
        qry = req['query']
    except IndexError:
        qry = "plot"

    data = []
    for i, x in enumerate(ndata):
        if i > (len(ndata) - qnt):  # offset
            if x[0] is not '':
                data.append(x)


    type = [int(x[0]) for x in data]
    src = [x[1] for x in data]

    if qry == "plot":
        return json.dumps({'success': 1, 'data': [sum(type)]})
    elif qry == "maps":
        return maps(src)
    else:
        return

def start():
    app.run(host=host, port=port, debug=False)
