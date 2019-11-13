
import ast
import json
import sys

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        tree = json.loads(f.read())
    body = tree['body']
    for stmt in body:
        print(stmt)
        print("\n\n")
