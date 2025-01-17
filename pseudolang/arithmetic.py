from .data_types import Stack

def applyOperator(operator, a, b):
    if operator == "+":
        return a + b
    if operator == "-":
        return a - b
    if operator == "*":
        return a * b
    if operator == "/":
        return a / b

def precedence(operator):
    # if operator == "(" or operator == ")":
    #     return 9
    if operator == "*" or operator == "/":
        return 2
    if operator == "+" or operator == "-":
        return 1
    return 0

def evaluate_expression(tokens : str):
    values = Stack(256)
    operators = Stack(256)
    was_digit = False

    for token in tokens:
        print(values, operators)
        if token == "(":
            operators.push(token)
        elif token.isdigit():
            if was_digit:
                values.top += token
            else:
                values.push(token)
            was_digit = True
        elif token == ")":
            print("Back")
    
    return values.top

print(evaluate_expression("(10+44)/2"))