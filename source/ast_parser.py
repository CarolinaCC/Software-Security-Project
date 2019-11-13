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
        Operator := + | - | / | * | % | or | and (? what else)
    '''
    @staticmethod
    def parse_from_node(node: dict):
        pass


class Identifier(Expression):
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def parse_from_node(node: dict):
        pass


class Literal(Expression):
    def __init__(self, val):
        self.val = val

    @staticmethod
    def parse_from_node(node: dict):
        pass


class AssignmentExpression(Statement):
    def __init__(self, left_val: Identifier, right_val: Expression):
        self.left_val = left_val
        self.right_val = right_val

    @staticmethod
    def parse_from_node(node: dict):
        print('Found AssignmentExpression')


class DoubleExpression(Expression):
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


def parse_node(node):
    if(node['ast_type'] == "Assign"):
        return AssignmentExpression.parse_from_node(node)

def parse(file_path):
    prog = list()
    with open(file_path, 'r') as f:
        tree = json.load(f)
    for node in tree['body']:
        prog.append(parse_node(node))


if __name__ == "__main__":
    parse(sys.argv[1])
