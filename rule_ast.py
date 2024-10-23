class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # 'operator' or 'operand'
        self.left = left       # Left child for binary operations
        self.right = right     # Right child for binary operations
        self.value = value     # Value for operand nodes (condition)

    def __repr__(self):
        if self.type == 'operator':
            return f"({self.left} {self.value} {self.right})"
        else:
            return str(self.value)