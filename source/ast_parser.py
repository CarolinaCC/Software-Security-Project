#!/bin/python3

import json
import sys

class Statement:
    '''
        Statement := Expression | If | If Else | While
    '''
    @staticmethod
    def parse_from_node(node: dict):
        pass



class Expression(Statement):
    '''
        In Python every Expression can be a Statement
        Expression := Literal | Identifier | Expression Operator Expression | not Expression | Function(Args)
        Operator := + | - | / | * | % | or | ** | // | == | and (? what else)
    '''
    @staticmethod
    def parse_from_node(node: dict):
        pass



class Identifier(Expression):
    '''
        An Identifier is a program variable id
    '''
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"{self.name}"

    @staticmethod
    def parse_from_node(node: dict):
        name = node['id']
        return Identifier(name)



class Literal(Expression):
    '''
        A literal is a constant value (like 3 or "Hello world")
        Literal := Num | Str
    '''
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return f"{self.val}"

    @staticmethod
    def parse_from_node(node: dict):
        ast_type = node['ast_type']
        if ast_type == "Str":
            return Literal(node['s'])
        elif ast_type == "Num":
            return Literal(node['n']['n'])
        else:
            #should never happen
            return None



class AssignExpression(Statement):
    def __init__(self, left_val: Identifier, right_val: Expression):
        self.left_val = left_val
        self.right_val = right_val

    def __repr__(self):
        return f"{self.left_val} := {self.right_val}"

    @staticmethod
    def parse_from_node(node: dict):
        left_val = parse_node_expr_value(node['targets'][0])
        right_val = parse_node_expr_value(node['value'])
        return AssignExpression(left_val, right_val)



class DoubleExpression(Expression):
    '''
        A DoubleExpression is an operation of two or more expressions
    '''
    def __init__(self, left_val: Expression, right_val: Expression, operator: str):
        self.left_val = left_val
        self.right_val = right_val
        self.operator = operator

    @staticmethod
    def parse_from_node(node: dict):
        pass



class UnaryExpression(Expression):
    '''
        UnaryExpression := not Expression
    '''
    def __init__(self, left_operator: str, right_val: Expression):
        self.left_operator = left_operator
        self.right_val = right_val

    @staticmethod
    def parse_from_node(node: dict):
        pass



class FunctionCall(Expression):
    '''
    FunctionCall:= name(Args)
    Args := Args , Expression | Expression | Empty
    '''
    def __init__(self, name: str, args: list): #args list of expressions
        self.name = name
        self.args = args

    @staticmethod
    def parse_from_node(node: dict):
        pass



class IfExpression(Statement):
    def __init__(self, cond: Expression, body: list, else_body: list):
        #body, else_body list of statements
        self.cond = cond
        self.body = body
        self.else_body = else_body #if no else else_body should be None

    @staticmethod
    def parse_from_node(node: dict):
        pass



class WhileExpression(Statement):
    def __init__(self, cond: Expression, body: list): #body: list of statements
        self.cond = cond
        self.body = body

    @staticmethod
    def parse_from_node(node: dict):
        pass


def parse_node_expr_value(node):
    if node['ast_type'] == 'Name':
        return Identifier.parse_from_node(node)
    if node['ast_type'] in ('Str', 'Num'):
        return Literal.parse_from_node(node)
    return None

def parse_node(node):
    if node['ast_type'] == "Assign":
        return AssignExpression.parse_from_node(node)
    if node['ast_type'] == 'Name':
        return Identifier.parse_from_node(node)
    #A statement that is just an expression
    if node['ast_type'] == 'Expr':
        return parse_node_expr_value(node["value"])
    return None


def parse(file_path):
    prog = list()
    with open(file_path, 'r') as f:
        tree = json.load(f)
    for node in tree['body']:
        stmt = parse_node(node)
        print(stmt)
        prog.append(stmt)



if __name__ == "__main__":
    parse(sys.argv[1])
