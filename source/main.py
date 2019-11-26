import json
import sys
import operator
import pattern_parser
import ast_parser
import copy


def prog_eval(patterns, prog, variables):
    if prog == []:
        return
    if isinstance(prog[0], ast_parser.IfExpression):
    	prog_eval(patterns, prog[0].body + prog[1:], copy.deepcopy(variables))
    	prog_eval(patterns, prog[0].else_body + prog[1:], copy.deepcopy(variables))

    if isinstance(prog[0], ast_parser.WhileExpression):
    	# while body will run twice
    	prog_eval(patterns, 3 * prog[0].body + prog[1:], copy.deepcopy(variables))
    	prog_eval(patterns, prog[1:], copy.deepcopy(variables))
    else:
    	prog[0].eval(variables, patterns)
    	prog_eval(patterns, prog[1:], variables)

if __name__ == "__main__":
    patterns = pattern_parser.parse(sys.argv[1])
    prog = ast_parser.parse(sys.argv[2])
    variables = {}
    prog_eval(patterns, prog, variables)
    unique_list = []
    for vuln in ast_parser.found_vulnerabilities:
        if vuln not in unique_list:
            unique_list.append(vuln)
    for vuln in unique_list:
        print(vuln)

    #for statement in prog:
    #    statement.eval(variables, patterns)
    #for variable in variables:
        #print(f"variable {variable} : {variables[variable]}")
