#!/bin/python3

import json
import sys

class Vulnerability:
    def __init__(self, sources: set, sanitizers: set, sinks: set):
        self.sources = set(sources)
        self.sanitizers = set(sanitizers)
        self.sinks = set(sinks)

    def add(self, sources: set, sanitizers: set, sinks: set):
        self.sources = self.sources.union(sources)
        self.sanitizers = self.sanitizers.union(sanitizers)
        self.sinks = self.sinks.union(sinks)

    def __str__(self):
        return f'\n\tsources: {str(self.sources)},\n\tsanitizers: {str(self.sanitizers)},\n\tsinks: {str(self.sinks)}\n \n'

    def __repr__(self):
        return self.__str__()

def parse(file_path: str) -> dict:
    #load json
    with open(file_path, 'r') as f:
        patterns = json.load(f)

    vulnerabilities = dict()

    for pattern in patterns:
        vulnerability = pattern['vulnerability']
        if not vulnerability in vulnerabilities:
            vulnerabilities[vulnerability] = Vulnerability(pattern['sources'], pattern['sanitizers'], pattern['sinks'])
        else:
            vulnerabilities[vulnerability].add(pattern['sources'], pattern['sanitizers'], pattern['sinks'])
    return vulnerabilities

if __name__ == '__main__':
    print(parse(sys.argv[1]))
