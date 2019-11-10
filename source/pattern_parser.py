#!/bin/python3

import json

def parse(file_path: str) -> dict:
    # Loads json from file to variable
    with open(file_path, 'r') as f:
        patterns = json.load(f)

    # Looks for repeated vulnerabilities and joins them into one
    to_remove = set()
    for number, pattern in enumerate(patterns):
        for i in range(number+1, len(patterns)):
            if patterns[i]['vulnerability'] == pattern['vulnerability']:
                to_remove.add(number)
                patterns[i]['sources'].append(pattern['sources'])
                patterns[i]['sanitizers'].append(pattern['sanitizers'])
                patterns[i]['sinks'].append(pattern['sinks'])
    for i in to_remove:
        del patterns[i]

    print(patterns)

if __name__ == '__main__':
    import sys
    parse(sys.argv[1])

