#!/bin/python
from event_log_parser import parse_events
from layout_parser import collect_layout_nodes

def check_inside(point, top_left, bottom_right):
    if top_left[0] <= point[0] and top_left[1] <= point[1]:
        if bottom_right[0] >= point[0] and bottom_right[1] >= point[1]:
            return True
    return False

def collect_counters(layout_filename, event_log):
    events = parse_events(event_log)
    nodes = collect_layout_nodes(layout_filename)
    
    counters = {}

    for node in nodes:
        counters[node.index] = {'type' : node.class_name, 'label' : node.text, 'events' : 0} 


    for node in nodes:
        for event in events:
            event_point = (event.x, event.y)
            if check_inside(event_point, node.top_left, node.bottom_right):
                counters[node.index]['events'] += 1
    
    return counters
   

counters = collect_counters('layout.xml', 'event-log.txt')

for key in counters.keys():
    print('Id: ' + str(key) + ' ', end='')
    print(counters[key])
