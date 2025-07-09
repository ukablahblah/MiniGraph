# ast_to_ir.py

import json
from ir import IRNode, IRGraph

def load_ast(path):
    with open(path) as f:
        return json.load(f)

def ast_to_ir(ast):
    graph = IRGraph()

    for stmt in ast:
        if stmt["type"] == "assign":
            var = stmt["var"]
            expr = stmt["expr"]

            if expr["type"] == "op":
                op = expr["name"]
                args = expr["args"]
                shape = None

                if op == "input":
                    shape = tuple(map(int, args))
                    args = []  # no input dependencies
                node = IRNode(op_type=op, name=var, inputs=args, shape=shape)
                graph.add_node(node)

        elif stmt["type"] == "output":
            # Output node (optional: could wrap in IRNode or treat as metadata)
            pass

    return graph

if __name__ == "__main__":
    ast = load_ast("ast_samples/simple_ast.json")
    graph = ast_to_ir(ast)

    with open("ir_samples/simple_ir.json", "w") as f:
        json.dump(graph.to_json(), f, indent=2)

    with open("ir_samples/simple_ir.dot", "w") as f:
        f.write(graph.to_dot())

    print("IR written to ir_samples/")
