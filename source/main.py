import json
import sys
import operator
import pattern_parser
import ast_parser
import copy

def prog_eval(patterns, prog, variables):
    if prog == []:
        return
    elif isinstance(prog[0], ast_parser.IfExpression):
        #print("if")
        prog_eval(patterns, prog[0].body + prog[1:], copy.deepcopy(variables))
        #print("else")
        prog_eval(patterns, prog[0].else_body + prog[1:], copy.deepcopy(variables))
    elif isinstance(prog[0], ast_parser.WhileExpression):
        #print("While true")
        prog_eval(patterns, prog[0].body + prog[0].body + prog[1:], copy.deepcopy(variables))
        #print("No while")
        prog_eval(patterns, prog[1:], copy.deepcopy(variables))
    else:
        prog[0].eval(variables, patterns)
        prog_eval(patterns, prog[1:], variables)

if __name__ == "__main__":
    patterns = pattern_parser.parse(sys.argv[1])
    prog = ast_parser.parse(sys.argv[2])
    variables = {}
    prog_eval(patterns, prog, variables)
    #for statement in prog:
    #    statement.eval(variables, patterns)
    #for variable in variables:
        #print(f"variable {variable} : {variables[variable]}")
