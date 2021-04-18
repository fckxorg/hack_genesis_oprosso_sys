from flask import Flask, send_from_directory
from flask import request
import subprocess
import multiprocessing
import json
import time

app = Flask(__name__)

record_process = None 
xml_dump_process = None
record_file = None
filename = 'telemetry/event-log.txt'


def xml_dumper():
    xml_dumps_count = 0
    while(True):
        xml = open('telemetry/' + str(xml_dumps_count) + '.xml', 'w')
        subprocess.Popen(['adb', 'exec-out', 'uiautomator', 'dump', '/dev/tty'], stdout=xml).wait()
        xml.close()

        png = open('telemetry/' + str(xml_dumps_count) + '.png', 'w')
        subprocess.Popen(['adb', 'exec-out', 'screencap', '-p'], stdout=png).wait()
        png.close()

        xml_dumps_count += 1
        time.sleep(0.3)

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
    global xml_dump_process
    global record_file

    record_file = open(filename, 'w')
    record_process = subprocess.Popen(args=['adb', 'shell', 'getevent', '-lt'], stdout=record_file)
    xml_dump_process = multiprocessing.Process(target=xml_dumper)
    xml_dump_process.start()
    return 'Ok'

@app.route('/stop', methods=['GET']) # stop recording
def stop_event_record():
    global record_process
    record_process.terminate()
    xml_dump_process.terminate()
    record_file.close()
    return 'Ok'

@app.route('/fetch', methods=['GET']) # fetch recorded data
def fetch_event_record():
    subprocess.call(['tar', 'cvf', 'telemetry.tar', 'telemetry/'])
    return send_from_directory('.', 'telemetry.tar')

