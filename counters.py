#!/bin/python
from event_log_parser import parse_events, batch_events
from layout_parser import collect_layout_nodes
from glob import glob

def check_inside(point, top_left, bottom_right):
    if top_left[0] <= point[0] and top_left[1] <= point[1]:
        if bottom_right[0] >= point[0] and bottom_right[1] >= point[1]:
            return True
    return False

def collect_counters(layouts, event_log):
    events = parse_events(event_log)
    nodes = []

    for layout in layouts:
        nodes.append(collect_layout_nodes(layout))
    per_view_events = batch_events(1, len(layouts), events)
    
    counters = {}

    for view in range(len(nodes)):
        for node_idx in range(len(nodes[view])):
            node = nodes[view][node_idx]
            counters[str(view) + '.' + str(node_idx)] = {'type' : node.class_name, 'label' : node.text, 'events' : 0} 

    
    
    for view_idx in range(len(per_view_events)):
        for event in per_view_events[view_idx]:
            for node_idx in range(len(nodes[view_idx])):
                node = nodes[view_idx][node_idx]
                event_point = (event.x, event.y)
                if check_inside(event_point, node.top_left, node.bottom_right):
                    counters[str(view_idx) + '.' + str(node_idx)]['events'] += 1
    
    return counters
   

views = glob('telemetry/*.xml')
counters = collect_counters(views, 'event-log.txt')

for key in counters.keys():
    print('Id: ' + str(key) + ' ', end='')
    print(counters[key])
