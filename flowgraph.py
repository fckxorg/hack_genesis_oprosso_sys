#!/bin/python
from graphviz import Digraph
from glob import glob
from layout_parser import compare_xml_trees


def create_flowgraph(dir_path, output):
    dot = Digraph(comment='Flow Chart')
    screens = sorted(glob(dir_path + '*.png'))
    xmls = sorted(glob(dir_path + '*.xml'))

    last_node = -1

    for idx in range(len(screens)):
        existing_id = -1

        for loaded_id in range(idx):
            if compare_xml_trees(xmls[loaded_id], xmls[idx]):
                existing_id = loaded_id
                break

        if existing_id == -1:
            dot.node(str(idx), 'Default', {'image': screens[idx], 'shape' : 'rect'})
            existing_id = idx

        if last_node != -1:
            dot.edge(str(last_node), str(existing_id))
        last_node = existing_id

    dot.render(output)

create_flowgraph('testflow/', 'flowchart.png')
        

