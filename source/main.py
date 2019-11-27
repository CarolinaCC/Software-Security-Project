import json
import sys
import copy
import pattern_parser
import ast_parser

def prog_eval_no_mem(patterns, prog, variables, stack):
    if prog == []:
        return
    if isinstance(prog[0], ast_parser.IfExpression):
        ast_parser.push_stack(stack, prog[0].eval(variables, patterns, stack))
        prog_eval_no_mem(patterns, prog[0].body + [ast_parser.EndCond()] + prog[1:], copy.deepcopy(variables), copy.deepcopy(stack))
        prog_eval_no_mem(patterns, prog[0].else_body + [ast_parser.EndCond()] + prog[1:], copy.deepcopy(variables), copy.deepcopy(stack))

    elif isinstance(prog[0], ast_parser.WhileExpression):
        prog_eval_no_mem(patterns, prog[1:], copy.deepcopy(variables), copy.deepcopy(stack))
        ast_parser.push_stack(stack, prog[0].eval(variables, patterns, stack))
        prog_eval_no_mem(patterns, 3 * prog[0].body + [ast_parser.EndCond()] +prog[1:], copy.deepcopy(variables), copy.deepcopy(stack))
    else:
        prog[0].eval(variables, patterns, stack)
        prog_eval_no_mem(patterns, prog[1:], variables, stack)



def prog_eval(patterns, prog, variables, stack, memory):
    if prog == []:
        return
    if isinstance(prog[0], ast_parser.IfExpression):
        cond_val = None
        cond_val = prog[0].get_val(memory)
        ast_parser.push_stack(stack, prog[0].eval(variables, patterns, stack))

        #condition value is not known
        if cond_val == None:
            prog_eval(patterns, prog[0].body + [ast_parser.EndCond()] + prog[1:], copy.deepcopy(variables), copy.deepcopy(stack), memory)
            prog_eval(patterns, prog[0].else_body + [ast_parser.EndCond()] + prog[1:], copy.deepcopy(variables), copy.deepcopy(stack), memory)

        #condition is true, only if executes
        elif cond_val == True:
            prog_eval(patterns, prog[0].body + [ast_parser.EndCond()] + prog[1:], copy.deepcopy(variables), copy.deepcopy(stack), memory)

        #condition is false, only else executes
        else:
            prog_eval(patterns, prog[0].else_body + [ast_parser.EndCond()] + prog[1:], copy.deepcopy(variables), copy.deepcopy(stack), memory)

    elif isinstance(prog[0], ast_parser.WhileExpression):
        #assume while cond is false
        prog_eval(patterns, prog[1:], copy.deepcopy(variables), copy.deepcopy(stack), memory)
        #assume while cond is true (execute 3 times for all possible vulnerabilities that might be encoded)
        ast_parser.push_stack(stack, prog[0].eval(variables, patterns, stack))
        prog_eval(patterns, 3 * prog[0].body + [ast_parser.EndCond()] +prog[1:], copy.deepcopy(variables), copy.deepcopy(stack), memory)

    else:
        prog[0].get_val(memory)
        prog[0].eval(variables, patterns, stack)
        prog_eval(patterns, prog[1:], variables, stack, memory)

if __name__ == "__main__":
    patterns = pattern_parser.parse(sys.argv[2])
    prog = ast_parser.parse(sys.argv[1])
    variables = {}
    stack = []
    use_val = False
    if "advanced" in sys.argv[3:]:
        prog_eval(patterns, prog, variables, stack, dict())
    else:
        prog_eval_no_mem(patterns, prog, variables, stack)

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

    with open(sys.argv[1][:-4] + "output.json", "w") as f:
        if "debug" not in sys.argv[3:]:
            json.dump(to_file, f)
        else:
            json.dump(unique_list, f)
