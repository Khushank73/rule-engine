import re
from rule_ast import Node

def create_rule(rule_string):
    # Update the regex to correctly capture attribute, operator, and value
    tokens = re.findall(r"(\w+)\s*(>=|<=|>|<|=)\s*(\d+|\w+)|AND|OR|\(|\)", rule_string)
    
    def parse_expression(tokens):
        stack = []
        for token in tokens:
            if token and token[0]:  # Ensure it's not an empty match
                attr, op, value = token[0], token[1], token[2]  # Unpacking matched groups
                stack.append(Node('operand', value=f"{attr} {op} {value}"))
            elif token == ')':
                right = stack.pop()
                op = stack.pop()
                left = stack.pop()
                stack.pop()  # Remove '('
                stack.append(Node('operator', left, right, op))
            elif token in ['AND', 'OR']:
                stack.append(token)
        return stack[0] if stack else None

    return parse_expression(tokens)


def evaluate_node(node, data):
    if node.type == 'operand':
        # Now node.value is a string like "age > 30"
        attr, op, value = node.value.split()  # Unpacking the string
        value = int(value) if value.isdigit() else value.strip("'")

        # Apply condition based on operator
        if op == '>':
            return data[attr] > value
        elif op == '<':
            return data[attr] < value
        elif op == '>=':
            return data[attr] >= value
        elif op == '<=':
            return data[attr] <= value
        elif op == '=':
            return data[attr] == value
    elif node.type == 'operator':
        left_result = evaluate_node(node.left, data)
        right_result = evaluate_node(node.right, data)
        if node.value == 'AND':
            return left_result and right_result
        elif node.value == 'OR':
            return left_result or right_result



def evaluate_rule(ast, data):
    return evaluate_node(ast, data)