import json
import sys
import operator
import pattern_parser
import ast_parser
import copy


def prog_eval(patterns, prog, variables, stack):
    if prog == []:
        return
    elif isinstance(prog[0], ast_parser.IfExpression):
        ast_parser.push_stack(stack, prog[0].eval(variables, patterns, stack))
        prog_eval(patterns, prog[0].body + [ast_parser.EndCond()] + prog[1:], copy.deepcopy(variables), copy.deepcopy(stack))
        prog_eval(patterns, prog[0].else_body + [ast_parser.EndCond()] + prog[1:], copy.deepcopy(variables), copy.deepcopy(stack))

    elif isinstance(prog[0], ast_parser.WhileExpression):
    	# while body running trice catches all possible vulnerabilities
        prog_eval(patterns, prog[1:], copy.deepcopy(variables), copy.deepcopy(stack))
        ast_parser.push_stack(stack, prog[0].eval(variables, patterns, stack))
        prog_eval(patterns, 3 * prog[0].body + [ast_parser.EndCond()] +prog[1:], copy.deepcopy(variables), copy.deepcopy(stack))

    else:
        prog[0].eval(variables, patterns, stack)
        prog_eval(patterns, prog[1:], variables, stack)

if __name__ == "__main__":
    patterns = pattern_parser.parse(sys.argv[1])
    prog = ast_parser.parse(sys.argv[2])
    variables = {}
    stack = []
    prog_eval(patterns, prog, variables, stack)
    unique_list = []
    to_file = []
    for vuln in ast_parser.found_vulnerabilities:
        if vuln not in unique_list:
            unique_list.append(vuln)

            to_file.append({"vulnerability": vuln["vuln"], "source": vuln["source"], "sink": vuln["sink"], "sanitizer": vuln["sanitizer"]})

    with open(sys.argv[2][:-4] + "output.json", "w") as f:
        if len(sys.argv) == 3:
            f.write(str(to_file))
        elif len(sys.argv) == 4 and sys.argv[3] == "debug":
            f.write(str(unique_list))
        #for vuln in unique_list:
        #    f.write(str(vuln))
