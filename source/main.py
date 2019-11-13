import json
import sys
import operator
import pattern_parser
import ast_parser


if __name__ == "__main__":
    patterns = pattern_parser.parse(sys.argv[1])
    #prog = ast_parser.parse(sys.argv[2])
