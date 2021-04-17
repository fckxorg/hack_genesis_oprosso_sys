#!/bin/python
from bs4 import BeautifulSoup as bs
import lxml

class Node:
    def __init__(self, keys):
        self.bounds = keys['bounds']
        self.checkable = keys['checkable']
        self.checked = keys['checked']
        self.class_name = keys['class']
        self.clickable = keys['clickable']
        self.content_desc = keys['content-desc']
        self.enabled = keys['enabled']
        self.focusable = keys['focusable']
        self.focused = keys['focused']
        self.index = keys['index']
        self.scrollable = keys['scrollable']
        self.selected = keys['selected']
        self.text = keys['text']
        
        corners = self.bounds.split(']')
        self.top_left = [int(point) for point in corners[0][1:].split(',')]
        self.bottom_right = [int(point) for point in corners[1][1:].split(',')]
    

def collect_layout_nodes(filename):
    with open('layout.xml', 'r') as layout:
        content = layout.read()
        bs_content = bs(content, 'lxml')

        layout_nodes = bs_content.find_all('node')
        
        nodes = []
        for node in layout_nodes:
            nodes.append(Node(node))
        return nodes
