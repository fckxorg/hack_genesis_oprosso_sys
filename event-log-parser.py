#!/bin/python

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

with open('event-log.txt', 'r') as log:
    events = [line for line in log.readlines() if line[0] == '[']
    
    events = filter_params(events, 'MAJOR') # remove sensor resolution info
    events = filter_params(events, 'PRESSURE') # remove pressure info
    events = filter_params(events, 'TRACKING_ID') # remove info about instrument (finger) i
    events = remove_device_name(events)
    events = remove_event_shortname(events)

    events = remove_linebreaks(events) # remove linebreaks as they are not needed

    for line in events:
        print(line)
