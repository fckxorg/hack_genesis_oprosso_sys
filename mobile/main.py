from flask import Flask
from flask import request
import subprocess
import json

app = Flask(__name__)

record_process = None 
record_file = None
filename = 'event-log.txt'

@app.route('/pair', methods=['GET']) # invoke pairing with android device
def pair_with_device():
    args = request.args.to_dict()
    return_code = subprocess.call(['adb', 'pair', args['addr'], args['code']])
    
    if return_code == 0:
        return 'Ok'
    else:
        return 'Error ' + str(return_code)

@app.route('/connect', methods=['GET']) # connect to remote device
def connect_to_device():
    args = request.args.to_dict()
    return_code = subprocess.call(['adb', 'connect', args['addr']])
    
    if return_code == 0:
        return 'Ok'
    else:
        return 'Error ' + str(return_code)

@app.route('/start', methods=['GET']) # start recording events
def start_event_record():
    global record_process
    global record_file

    record_file = open(filename, 'w')
    record_process = subprocess.Popen(args=['adb', 'shell', 'getevent', '-lt'], stdout=record_file)
    return 'Ok'

@app.route('/stop', methods=['GET']) # stop recording
def stop_event_record():
    global record_process
    record_process.terminate()
    record_file.close()
    return 'Ok'

@app.route('/fetch', methods=['GET']) # fetch recorded data
def fetch_event_record():
    with open(filename, 'r') as record:
        raw_data = record.read()
        payload = {'events' : raw_data}
        return json.dumps(payload)
