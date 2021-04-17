#!/bin/python
from bs4 import BeautifulSoup as bs
from graphviz import Digraph
import lxml
import xml.etree.ElementTree as ET

node_counter = 0

class Node:
    def __init__(self, keys, idx):
        self.bounds = keys['bounds']
        self.checkable = keys['checkable']
        self.checked = keys['checked']
        self.class_name = keys['class']
        self.clickable = keys['clickable']
        self.content_desc = keys['content-desc']
        self.enabled = keys['enabled']
        self.focusable = keys['focusable']
        self.focused = keys['focused']
        self.index = idx
        self.scrollable = keys['scrollable']
        self.selected = keys['selected']
        self.text = keys['text']
        
        corners = self.bounds.split(']')
        self.top_left = [int(point) for point in corners[0][1:].split(',')]
        self.bottom_right = [int(point) for point in corners[1][1:].split(',')]

def prepare_xml(filename):
    with open(filename, 'r+', encoding='utf-8') as xml_file:
        content = xml_file.read()
        xml_file.seek(0)
        xml_file.truncate(0)
        xml_start = content.find('<')
        xml_end = content.rfind('>') + 1
        raw = content[xml_start : xml_end]
        xml_file.write(raw)
    

def collect_layout_nodes(filename):
    prepare_xml(filename)
    with open(filename, 'r') as layout:
        content = layout.read()
        bs_content = bs(content, 'lxml')

        layout_nodes = bs_content.find_all('node')
        
        nodes = []
        for idx in range(len(layout_nodes)):
            nodes.append(Node(layout_nodes[idx], idx))
        return nodes

def write_tree(node, dot, parent_id):
    global node_counter

    try:
        node_label = node.attrib['class']
    except KeyError:
        node_label = 'No class'
    dot.node(str(node_counter), node_label) 
    new_parent_id = node_counter
    node_counter += 1

    if parent_id != -1:
        dot.edge(str(parent_id), str(new_parent_id))

    for child in node:
        write_tree(child, dot, new_parent_id)

def dump_xml_tree(filename, output):
    prepare_xml(filename)
    dot = Digraph(comment='XML Tree')
    tree = ET.parse(filename)
    root = tree.getroot()
    write_tree(root, dot, -1)
    dot.render(output)


def get_children_count(node):
    counter = 0
    for child in node:
        counter += 1
    return counter

def compare_subtrees(fnode, snode):
    if get_children_count(fnode) != get_children_count(snode):
        return False

    for fchild, schild in zip(fnode, snode):
        try:
            fclass = fchild.attrib['class']
        except KeyError:
            fclass = None

        try:
            sclass = schild.attrib['class']
        except KeyError:
            sclass = None

        if fclass != sclass:
            return False
        if not compare_subtrees(fchild, schild):
            return False

    return True

def compare_xml_trees(first_xml, second_xml):
    prepare_xml(first_xml)
    prepare_xml(second_xml)

    ftree = ET.parse(first_xml)
    stree = ET.parse(second_xml)
    
    froot = ftree.getroot()
    sroot = stree.getroot()
    
    return compare_subtrees(froot, sroot)
