# ir.py

class IRNode:
    def __init__(self, op_type, name, inputs=None, shape=None):
        self.op_type = op_type  # e.g., "matmul", "relu", "input"
        self.name = name        # variable name (e.g., "x", "y", "z")
        self.inputs = inputs or []  # list of variable names (strings)
        self.shape = shape      # optional shape info (e.g., (2, 2))

    def __repr__(self):
        return f"{self.name} = {self.op_type}({', '.join(self.inputs)})"

class IRGraph:
    def __init__(self):
        self.nodes = []         # List of IRNode
        self.symbol_table = {}  # Maps variable names → IRNode

    def add_node(self, node):
        self.nodes.append(node)
        self.symbol_table[node.name] = node

    def to_dot(self):
        lines = ["digraph IR {"]
        for node in self.nodes:
            for inp in node.inputs:
                lines.append(f'  "{inp}" -> "{node.name}";')
        lines.append("}")
        return "\n".join(lines)

    def to_json(self):
        return [
            {
                "name": node.name,
                "op": node.op_type,
                "inputs": node.inputs,
                "shape": node.shape
            }
            for node in self.nodes
        ]
