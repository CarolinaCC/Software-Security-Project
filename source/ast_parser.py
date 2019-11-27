#!/bin/python3

import json
import sys
import copy
import operator

def execute_operator(a, b, op):
    if a == None or b == None:
        return None
    if op == "Mult":
        op = "mul"
    method = getattr(operator,  "__" + op.lower() + "__")
    return method(a,b)

def get_stack_vulnerabilities(stack: list) -> list:
    vulns = []
    for entry in stack:
        vulns += entry
    return vulns


def push_stack(stack: list, insert: list) -> list:
    for entry in insert:
        entry["source_type"] = "Implicit"

    stack.append(insert)


found_vulnerabilities = []


class Statement:
    '''
        Statement := Expression | If | If Else | While | Identifier = Expression
    '''
    @staticmethod
    def parse_from_node(node: dict):
        pass

    def eval(self, variables, patterns, stack):
        pass

    def get_val(self, memory: dict):
        pass

class Expression(Statement):
    '''
        In Python every Expression can be a Statement
        Expression := Literal | Identifier | Expression Operator Expression | not Expression | Function(Args) | Expression BooleanOperator Expression
        Operator := + | - | / | * | % | or | ** | // | == | and (? what else)
        BooleanOperator := and | or
    '''
    @staticmethod
    def parse_from_node(node: dict):
        pass

    def eval(self, variables, patterns, stack):
        pass

    def get_val(self, memory: dict):
        pass

class EndCond(Expression):

    def __init__(self):
        pass

    def eval(self, variables, patterns, stack):
        stack.pop()

    def get_val(self, memory: dict):
        return None

class Identifier(Expression):
    '''
        An Identifier is a program variable id
    '''
    def __init__(self, name: str, lineno: int, col_offset: int):
        self.name = name
        self.lineno = lineno
        self.col_offset = col_offset

    def __repr__(self):
        return f"{self.name}"

    @staticmethod
    def parse_from_node(node: dict):
        name = node['id']
        return Identifier(name, node["lineno"], node["col_offset"])

    @staticmethod
    def new_variable_eval(name, lineno, col_offset, patterns):
        new_var = []
        for vuln_name in patterns.keys():
            new_var.append({"vuln": vuln_name, "source": name, "source_lineno": lineno, \
            "source_col_offset": col_offset, "source_type" : "Explicit",
             "sanitizer": "", "sanitizer_lineno":0, "sanitizer_col_offset" : 0})
        return new_var

    def eval(self, variables, patterns, stack):
        if not self.name in variables:
            variables[self.name] = Identifier.new_variable_eval(self.name, self.lineno, self.col_offset, patterns)
        return copy.deepcopy(variables[self.name])

    def get_val(self, memory: dict):
        if self.name not in memory:
            return None
        return memory[self.name]

class Literal(Expression):
    '''
        A literal is a constant value (like 3 or "Hello world")
        Literal := Num | Str
    '''
    def __init__(self, val, lineno: int, col_offset: int):
        self.val = val
        self.lineno = lineno
        self.col_offset = col_offset

    def __repr__(self):
        return f"{self.val}"

    @staticmethod
    def parse_from_node(node: dict):
        ast_type = node['ast_type']
        if ast_type == 'Str':
            return Literal(node['s'], node["lineno"], node["col_offset"])
        if ast_type == 'Num':
            return Literal(node['n']['n'], node["lineno"], node["col_offset"])
        if ast_type == 'NameConstant':
            return Literal(eval(node["value"]), node["lineno"], node["col_offset"])
        #should never happen
        return None

    def eval(self, variables, patterns, stack):
        return []

    def get_val(self, memory: dict):
        return self.val

class AssignExpression(Statement):
    def __init__(self, left_val: Identifier, right_val: Expression, lineno: int, col_offset: int):
        self.left_val = left_val
        self.right_val = right_val
        self.lineno = lineno
        self.col_offset = col_offset

    def __repr__(self):
        return f"{self.left_val} := {self.right_val}"

    @staticmethod
    def parse_from_node(node: dict):
        left_val = parse_node_expr_value(node['targets'][0])
        right_val = parse_node_expr_value(node['value'])
        return AssignExpression(left_val, right_val, node["lineno"], node["col_offset"])

    def eval(self, variables, patterns, stack):
        variables[self.left_val.name] = self.right_val.eval(variables, patterns, stack) + get_stack_vulnerabilities(stack)
        return copy.deepcopy(variables[self.left_val.name])

    def get_val(self, memory: dict):
        memory[self.left_val.name] = self.right_val.get_val(memory)
        return memory[self.left_val.name]

class DoubleExpression(Expression):
    '''
        A DoubleExpression is an operation of two or more expressions
    '''
    def __init__(self, left_val: Expression, right_val: Expression, operator: str, lineno: int, col_offset: int):
        self.left_val = left_val
        self.right_val = right_val
        self.operator = operator
        self.lineno = lineno
        self.col_offset = col_offset

    def __repr__(self):
        return f"{self.left_val} {self.operator} {self.right_val}"

    @staticmethod
    def parse_from_node(node: dict):
        left_val = parse_node_expr_value(node["left"])
        right_val = parse_node_expr_value(node["right"])
        operator = node["op"]["ast_type"]
        return DoubleExpression(left_val, right_val, operator, node["lineno"], node["col_offset"])

    def eval(self, variables, patterns, stack):
        return self.left_val.eval(variables, patterns, stack) + self.right_val.eval(variables, patterns, stack)

    def get_val(self, memory: dict):
        return execute_operator(self.left_val.get_val(memory), self.right_val.get_val(memory), self.operator)

class AttributeExpression(Expression):
    '''
        A AttributeExpression
    '''
    def __init__(self, left_val: Expression, right_val: Expression, lineno: int, col_offset: int):
        self.left_val = left_val
        self.right_val = right_val
        self.lineno = lineno
        self.col_offset = col_offset

    def __repr__(self):
        return f"{self.right_val}.{self.left_val}"

    @staticmethod
    def parse_from_node(node: dict):
        left_val = Identifier(node["attr"], node["lineno"], node["col_offset"])
        right_val = parse_node_expr_value(node["value"])
        return AttributeExpression(left_val, right_val, node["lineno"], node["col_offset"])

    def eval(self, variables, patterns, stack):
        return self.left_val.eval(variables, patterns, stack) + self.right_val.eval(variables, patterns, stack)

    def get_val(self, memory: dict):
        return None

class CompareExpression(Expression):
    '''
        A CompareOperation is an
    '''
    def __init__(self, left_val: Expression, right_val: Expression, operator: str, lineno: int, col_offset: int):
        self.left_val = left_val
        self.right_val = right_val
        self.operator = operator
        self.lineno = lineno
        self.col_offset = col_offset

    def __repr__(self):
        return f"{self.left_val} {self.operator} {self.right_val}"

    @staticmethod
    def parse_from_node(node: dict):
        right_val = parse_node_expr_value(node["comparators"][0])
        left_val = parse_node_expr_value(node["left"])
        operator = node["ops"][0]["ast_type"]
        return CompareExpression(left_val, right_val, operator, node["lineno"], node["col_offset"])

    def eval(self, variables, patterns, stack):
        return self.left_val.eval(variables, patterns, stack) + self.right_val.eval(variables, patterns, stack)

    def get_val(self, memory: dict):
        return execute_operator(self.left_val.get_val(memory), self.right_val.get_val(memory), self.operator)

class BooleanExpression(Expression):
    '''
        A BooleanOperation is an operation of two or more expressions and a boolean operator
    '''
    def __init__(self, left_val: Expression, right_val: Expression, operator: str, lineno: int, col_offset: int):
        self.left_val = left_val
        self.right_val = right_val
        self.operator = operator
        self.lineno = lineno
        self.col_offset = col_offset

    def __repr__(self):
        return f"{self.left_val} {self.operator} {self.right_val}"

    @staticmethod
    def parse_from_node(node: dict):
        left_val = parse_node_expr_value(node["values"][0])
        right_val = parse_node_expr_value(node["values"][1])
        operator = node["op"]["ast_type"]
        return DoubleExpression(left_val, right_val, operator, node["lineno"], node["col_offset"])

    def eval(self, variables, patterns, stack):
        return self.left_val.eval(variables, patterns, stack) + self.right_val.eval(variables, patterns, stack)

    def get_val(self, memory: dict):
        return execute_operator(self.left_val.get_val(memory), self.right_val.get_val(memory), self.operator)

class UnaryExpression(Expression):
    '''
        UnaryExpression := not Expression
    '''
    def __init__(self, left_operator: str, right_val: Expression, lineno: int, col_offset: int):
        self.left_operator = left_operator
        self.right_val = right_val
        self.lineno = lineno
        self.col_offset = col_offset

    def __repr__(self):
        return f"{self.left_operator} {self.right_val}"

    @staticmethod
    def parse_from_node(node: dict):
        left_operator = node["op"]["ast_type"]
        right_val = parse_node_expr_value(node["operand"])
        return UnaryExpression(left_operator, right_val, node["lineno"], node["col_offset"])

    def eval(self, variables, patterns, stack):
        return self.right_val.eval(variables, patterns, stack)

    def get_val(self, memory: dict):
        val = self.right_val.get_val(memory)
        if (val == None):
            return None
        return operator.__not__(val)

class FunctionCall(Expression):
    '''
    FunctionCall:= name(Args)
    Args := Args , Expression | Expression | Empty
    '''
    def __init__(self, name: str, args: list, lineno: int, col_offset: int): #args list of expressions
        self.name = name
        self.lineno = lineno
        self.args = args
        self.col_offset = col_offset

    def __repr__(self):
        return f"{self.name}({self.args})"

    @staticmethod
    def parse_from_node(node: dict):
        name = node["func"]["attr" if "attr" in node["func"] else "id"]
        args = [parse_node_expr_value(arg) for arg in node["args"]]
        return FunctionCall(name, args, node["lineno"], node["col_offset"])

    def get_vulnerabilities(self, patterns):
        vulnerabilities = list()
        for name, vulnerability in patterns.items():
            if self.name in vulnerability.sources:
                vulnerabilities.append({"vuln": name, "source": self.name, \
                "source_lineno": self.lineno, "source_col_offset": self.col_offset,
                "source_type" : "Explicit",
                "sanitizer" : "", "sanitizer_lineno" : 0, "sanitizer_col_offset" : 0})
        return vulnerabilities

    def get_sanitizers(self, patterns):
        vulnerabilities = list()
        for name, vulnerability in patterns.items():
            if self.name in vulnerability.sanitizers:
                vulnerabilities.append(name)
        return vulnerabilities

    def get_sinks(self, patterns):
        vulnerabilities = list()
        for name, vulnerability in patterns.items():
            if self.name in vulnerability.sinks:
                vulnerabilities.append(name)
        return vulnerabilities

    def eval(self, variables, patterns, stack):
        vulnerabilities = []
        for arg in self.args:
            vulnerabilities += arg.eval(variables, patterns, stack)

        vulnerabilities += self.get_vulnerabilities(patterns)

        sanitized_vulnerabilities = self.get_sanitizers(patterns)
        for sanitized_vulnerability in sanitized_vulnerabilities:
            for vulnerability in vulnerabilities:
                if vulnerability["vuln"] == sanitized_vulnerability:
                    vulnerability["sanitizer"] = self.name
                    vulnerability["sanitizer_lineno"] = self.lineno
                    vulnerability["sanitizer_col_offset"] = self.col_offset

        for sink in self.get_sinks(patterns):
            for arg in self.args:
                for vulnerability in arg.eval(variables, patterns, stack):
                    if vulnerability["vuln"] == sink:
                        to_print = copy.deepcopy(vulnerability)
                        to_print["sink"] = self.name
                        to_print["sink_lineno"] = self.lineno
                        to_print["sink_col_offset"] = self.col_offset
                        found_vulnerabilities.append(to_print)
        return vulnerabilities

    def get_val(self, memory: dict):
        return None

class IfExpression(Statement):
    def __init__(self, cond: Expression, body: list, else_body: list, lineno: int, col_offset: int):
        #body, else_body list of statements
        self.cond = cond
        self.body = body
        self.else_body = else_body #if no else else_body should be Empty List
        self.lineno = lineno
        self.col_offset = col_offset

    def __repr__(self):
        return f"If {self.cond} then {self.body} else {self.else_body}"

    @staticmethod
    def parse_from_node(node: dict):
        cond = parse_node_expr_value(node["test"])
        body = []
        for sub_node in node["body"]:
            body.append(parse_node(sub_node))
        else_body = []
        for sub_node in node["orelse"]:
            else_body.append(parse_node(sub_node))
        return IfExpression(cond, body, else_body, node["lineno"], node["col_offset"])

    def eval(self, variables, patterns, stack):
        return self.cond.eval(variables, patterns, stack)

    def get_val(self, memory: dict):
        return self.cond.get_val(memory)

class WhileExpression(Statement):
    def __init__(self, cond: Expression, body: list, lineno: int, col_offset: int): #body: list of statements
        self.cond = cond
        self.body = body
        self.lineno = lineno
        self.col_offset = col_offset

    def __repr__(self):
        return f"While {self.cond} do {self.body}"

    @staticmethod
    def parse_from_node(node: dict):
        cond = parse_node_expr_value(node["test"])
        body = [parse_node(n) for n in node["body"]]
        return WhileExpression(cond, body, node["lineno"], node["col_offset"])

    def eval(self, variables, patterns, stack):
        return self.cond.eval(variables, patterns, stack)

    def get_val(self, memory: dict):
        return self.cond.get_val(memory)

def parse_node_expr_value(node):
    if node['ast_type'] == 'Compare':
        return CompareExpression.parse_from_node(node)
    if node['ast_type'] == 'Name':
        return Identifier.parse_from_node(node)
    if node['ast_type'] in ('Str', 'Num', 'NameConstant'):
        return Literal.parse_from_node(node)
    if node['ast_type'] == "UnaryOp":
        return UnaryExpression.parse_from_node(node)
    if node['ast_type'] == "BinOp":
        return DoubleExpression.parse_from_node(node)
    if node['ast_type'] == "BoolOp":
        return BooleanExpression.parse_from_node(node)
    if node["ast_type"] == "Call":
        return FunctionCall.parse_from_node(node)
    if node["ast_type"] == "Attribute":
        return AttributeExpression.parse_from_node(node)
    return None

def parse_node(node):
    #stmt -> Assign, Expr, if, while
    if node['ast_type'] == "Assign":
        return AssignExpression.parse_from_node(node)
    #A statement that is just an expression
    if node['ast_type'] == 'Expr':
        return parse_node_expr_value(node["value"])
    if node['ast_type'] == 'If':
        return IfExpression.parse_from_node(node)
    if node['ast_type'] == 'While':
        return WhileExpression.parse_from_node(node)
    return None


def parse(file_path):
    program = list()
    with open(file_path, 'r') as f:
        tree = json.load(f)
    for node in tree['body']:
        stmt = parse_node(node)
        program.append(stmt)
    return program


if __name__ == "__main__":
    mem = {}
    prog = parse(sys.argv[1])
    for statement in prog:
        print(f"{statement} = {statement.get_val(mem)}")
