import json
import sys
import operator
import pattern_parser
import ast_parser
import copy


def prog_eval(patterns, prog, variables, stack, use_val, memory):
    if prog == []:
        return
    elif isinstance(prog[0], ast_parser.IfExpression):
        cond_val = None
        if use_val:
            cond_val = prog[0].get_val(memory)
        ast_parser.push_stack(stack, prog[0].eval(variables, patterns, stack))
        if cond_val == None:
            #condition value is not known
            prog_eval(patterns, prog[0].body + [ast_parser.EndCond()] + prog[1:], copy.deepcopy(variables), copy.deepcopy(stack), use_val, memory)
            prog_eval(patterns, prog[0].else_body + [ast_parser.EndCond()] + prog[1:], copy.deepcopy(variables), copy.deepcopy(stack), use_val, memory)
        elif cond_val == True:
            #condition is true, only if executes
            prog_eval(patterns, prog[0].body + [ast_parser.EndCond()] + prog[1:], copy.deepcopy(variables), copy.deepcopy(stack), use_val, memory)
        else:
            #condition is false, only else executes
            prog_eval(patterns, prog[0].else_body + [ast_parser.EndCond()] + prog[1:], copy.deepcopy(variables), copy.deepcopy(stack), use_val, memory)

    elif isinstance(prog[0], ast_parser.WhileExpression):
        # while body running trice catches all possible vulnerabilities
        cond_val = None
        if use_val:
            cond_val = prog[0].get_val(memory)
        if cond_val == None:
            #condition value is not known
            prog_eval(patterns, prog[1:], copy.deepcopy(variables), copy.deepcopy(stack), use_val, memory)
            ast_parser.push_stack(stack, prog[0].eval(variables, patterns, stack))
            prog_eval(patterns, 3 * prog[0].body + [ast_parser.EndCond()] +prog[1:], copy.deepcopy(variables), copy.deepcopy(stack), use_val, memory)
        elif cond_val == True:
            #condition is true, only while body executes
            ast_parser.push_stack(stack, prog[0].eval(variables, patterns, stack))
            prog_eval(patterns, 3 * prog[0].body + [ast_parser.EndCond()] +prog[1:], copy.deepcopy(variables), copy.deepcopy(stack), use_val, memory)
        else:
            #condition is false, only rest of program executes
            prog_eval(patterns, prog[1:], copy.deepcopy(variables), copy.deepcopy(stack), use_val, memory)

    else:
        if use_val:
            prog[0].get_val(memory)
        prog[0].eval(variables, patterns, stack)
        prog_eval(patterns, prog[1:], variables, stack, use_val, memory)

if __name__ == "__main__":
    patterns = pattern_parser.parse(sys.argv[1])
    prog = ast_parser.parse(sys.argv[2])
    variables = {}
    stack = []
    use_val = False
    if "advanced" in sys.argv[3:]:
        use_val = True
    prog_eval(patterns, prog, variables, stack, use_val, dict())

    unique_list = []
    to_file = []
    
    print_flag = False
    if "print" in sys.argv[3:]:
        print_flag = True

    for vuln in ast_parser.found_vulnerabilities:
        if vuln not in unique_list:
            unique_list.append(vuln)
            to_file.append({"vulnerability": vuln["vuln"], "source": vuln["source"], "sink": vuln["sink"], "sanitizer": vuln["sanitizer"]})
            if print_flag:
                print(vuln)
    with open(sys.argv[2][:-4] + "output.json", "w") as f:
        if "debug" not in sys.argv[3:]:
            f.write(str(to_file))
        else:
            f.write(str(unique_list))
        #for vuln in unique_list:
        #    f.write(str(vuln))
