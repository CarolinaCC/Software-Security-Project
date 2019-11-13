#!/bin/python3

import json

def parse(file_path):
    with open(file_path,'r') as f:
        tree = json.load(f.read())
    print(tree)
    return
