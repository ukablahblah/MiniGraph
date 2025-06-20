from lark import Lark, Transformer, Tree
import json
import os

with open("grammar.lark") as f:
    grammar = f.read()

parser = Lark(grammar, parser="lalr")


class ASTBuilder(Transformer):
    def deep_transform(self, obj):
        if isinstance(obj, Tree):
            return self.transform(obj)
        elif isinstance(obj, list):
            return [self.deep_transform(x) for x in obj]
        elif isinstance(obj, dict):
            return {k: self.deep_transform(v) for k, v in obj.items()}
        else:
            return obj

    def start(self, children):
        return self.deep_transform(children)

    def assign_stmt(self, children):
        var, expr = children
        expr = self.deep_transform(expr)
        return self.deep_transform({"type": "assign", "var": str(var), "expr": expr})

    def output_stmt(self, children):
        (var,) = children
        return self.deep_transform({"type": "output", "var": str(var)})

    def op_call(self, children):
        name = children[0]
        args = children[1] if len(children) > 1 else []
        args = self.deep_transform(args)
        return self.deep_transform({"type": "op", "name": str(name), "args": args})


    def args(self, children):
        return [str(child) for child in children]

    def expr(self, children):
        (val,) = children
        return self.deep_transform(val)

    def NAME(self, token):
        return str(token)

    def NUMBER(self, token):
        return str(token)


def parse_dsl(code):
    tree = parser.parse(code)
    ast = ASTBuilder().transform(tree)

    # Debug: find any leftover Tree objects in AST
    def find_trees(obj):
        if isinstance(obj, Tree):
            print("Found untransformed Tree:", obj)
        elif isinstance(obj, list):
            for i in obj:
                find_trees(i)
        elif isinstance(obj, dict):
            for v in obj.values():
                find_trees(v)
    find_trees(ast)

    return ast

def parse_dsl(code):
    tree = parser.parse(code)
    return ASTBuilder().transform(tree)

if __name__ == "__main__":
    os.makedirs("ast_samples", exist_ok=True)
    with open("examples/simple.mg") as f:
        code = f.read()
    ast = parse_dsl(code)
    with open("ast_samples/simple_ast.json", "w") as out:
        json.dump(ast, out, indent=2)
    print("Parsed AST written to ast_samples/simple_ast.json")
