#!/bin/python3

import json

class Vulnerability:
    def __init__(self, sources: list, sanitizers: list, sinks: list):
        self.sources = set(sources)
        self.sanitizers = set(sanitizers)
        self.sinks = set(sinks)

    def add(self, sources: list, sanitizers: list, sinks: list):
        for source in sources:
            self.sources.add(source)
        for sanitizer in sanitizers:
            self.sanitizers.add(sanitizer)
        for sink in sinks:
            self.sinks.add(sink)

    def __str__(self):
        return f'sources: {str(self.sources)}, sanitizers: {str(self.sanitizers)}, sinks: {str(self.sinks)}'

    def __repr__(self):
        return f'sources: {str(self.sources)}, sanitizers: {str(self.sanitizers)}, sinks: {str(self.sinks)}'

def parse(file_path: str) -> dict:
    # Loads json from file to variable
    with open(file_path, 'r') as f:
        patterns = json.load(f)

    vulnerabilities = dict()
    for pattern in patterns:
        if not pattern['vulnerability'] in vulnerabilities:
            vulnerabilities[pattern['vulnerability']] = Vulnerability(pattern['sources'], pattern['sanitizers'], pattern['sinks'])
        else:
            vulnerabilities[pattern['vulnerability']].add(pattern['sources'], pattern['sanitizers'], pattern['sinks'])
    return vulnerabilities

if __name__ == '__main__':
    import sys
    print(parse(sys.argv[1]))
