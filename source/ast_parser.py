#!/bin/python3

import json
import sys

class Statement:
    '''
        Statement := Expression | If | If Else | While | Identifier = Expression
    '''
    @staticmethod
    def parse_from_node(node: dict):
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
        if ast_type == 'Str':
            return Literal(node['s'])
        if ast_type == 'Num':
            return Literal(node['n']['n'])
        if ast_type == 'NameConstant':
            return Literal(node["value"])
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


    def __repr__(self):
        return f"{self.left_val} {self.operator} {self.right_val}"

    @staticmethod
    def parse_from_node(node: dict):
        left_val = parse_node_expr_value(node["left"])
        right_val = parse_node_expr_value(node["right"])
        operator = node["op"]["ast_type"]
        return DoubleExpression(left_val, right_val, operator)

class BooleanExpression(Expression):
    '''
        A BooleanOperation is an operation of two or more expressions and a boolean operator
    '''
    def __init__(self, left_val: Expression, right_val: Expression, operator: str):
        self.left_val = left_val
        self.right_val = right_val
        self.operator = operator


    def __repr__(self):
        return f"{self.left_val} {self.operator} {self.right_val}"

    @staticmethod
    def parse_from_node(node: dict):
        left_val = parse_node_expr_value(node["values"][0])
        right_val = parse_node_expr_value(node["values"][1])
        operator = node["op"]["ast_type"]
        return DoubleExpression(left_val, right_val, operator)


class UnaryExpression(Expression):
    '''
        UnaryExpression := not Expression
    '''
    def __init__(self, left_operator: str, right_val: Expression):
        self.left_operator = left_operator
        self.right_val = right_val

    def __repr__(self):
        return f"{self.left_operator} {self.right_val}"

    @staticmethod
    def parse_from_node(node: dict):
        left_operator = node["op"]["ast_type"]
        right_val = parse_node_expr_value(node["operand"])
        return UnaryExpression(left_operator, right_val)


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
        self.else_body = else_body #if no else else_body should be Empty List

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
        return IfExpression(cond, body, else_body)



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
    if node['ast_type'] in ('Str', 'Num', 'NameConstant'):
        return Literal.parse_from_node(node)
    if node['ast_type'] == "UnaryOp":
        return UnaryExpression.parse_from_node(node)
    if node['ast_type'] == "BinOp":
        return DoubleExpression.parse_from_node(node)
    if node['ast_type'] == "BoolOp":
        return BooleanExpression.parse_from_node(node)
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
