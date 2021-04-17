#!/bin/python

class Event:
    def __init__(self, x, y, btn, time):
        self.x = x
        self.y = y
        self.btn = btn
        self.time = time

def filter_params(lines, word):
    return [line for line in lines if word not in line]

def remove_linebreaks(lines):
    return [line[:-1] for line in lines]

def remove_device_name(lines):
    filtered = []

    for line in lines:
        dev_name_start = line.find('/dev')
        dev_name_end = line.find(':') + 1

        new_line = line[:dev_name_start] + line[dev_name_end:]
        filtered.append(new_line)

    return filtered

def remove_event_shortname(lines):
    filtered = []
    
    for line in lines:
        e_sh_s = line.find('EV')
        e_sh_e = line[e_sh_s:].find(' ') + 1 + e_sh_s

        new_line = line[:e_sh_s] + line[e_sh_e:]
        filtered.append(new_line)

    return filtered

def not_none(*args):
    for arg in args:
        if arg is None:
            return False
    return True

def collect(lines):
    events = [] 
    x = None
    y = None
    time = None
    btn = None

    sec_start = None

    for line in lines:
        if 'SYN_REPORT' in line:
            if not_none(x, y, time):
                events.append(Event(x, y, btn, time))
            x = None
            y = None
            time = None
            btn = None

        if 'POSITION_X' in line:
            x = int(line.split()[3], 16)
        if 'POSITION_Y' in line:
            y = int(line.split()[3], 16)

        if 'BTN_TOUCH' in line:
            state = line.split()[3] 
            
            if state == 'UP':
                btn = 0
            if state == 'DOWN':
                btn = 1
        
        # gather time stamp
        timestamp = line.split()[1][:-1] 
        sec, microsec = [int(x) for x in timestamp.split('.')]
        
        if sec_start is None:
            sec_start = sec
        
        adj_sec = sec - sec_start
        time = str(adj_sec) + '.' + str(microsec) 
    return events


def parse_events(filename):
    with open(filename, 'r') as log:
        events = [line for line in log.readlines() if line[0] == '[']
        
        events = filter_params(events, 'MAJOR') # remove sensor resolution info
        events = filter_params(events, 'PRESSURE') # remove pressure info
        events = filter_params(events, 'TRACKING_ID') # remove info about instrument (finger) i
        events = remove_device_name(events)
        events = remove_event_shortname(events)

        events = remove_linebreaks(events) # remove linebreaks as they are not needed

        event_objects = collect(events)

        return event_objects

events = parse_events('event-log.txt')

for event in events:
    print(event.__dict__)

