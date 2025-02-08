from __future__ import annotations

import ast
import inspect
import textwrap
from collections.abc import Callable


class TranspilerError(Exception):
    """Exception raised when transpilation fails or encounters ambiguous syntax."""

    def __init__(self, message: str, node: ast.AST | None = None):
        self.node = node
        if node and hasattr(node, "lineno"):
            message = f"Line {node.lineno}: {message}"  # type: ignore
        super().__init__(message)


class PythonToJSVisitor(ast.NodeVisitor):
    def __init__(self):
        self.js_lines = []  # Accumulate lines of JavaScript code.
        self.indent_level = 0  # Track current indent level for readability.
        self.declared_vars = (
            set()
        )  # Track declared variables to avoid redeclaring with 'let'

    def indent(self) -> str:
        return "    " * self.indent_level

    # === Function Definition ===
    def visit_FunctionDef(self, node: ast.FunctionDef):  # noqa: N802
        # Extract parameter names. (Later we could add type hint checks.)
        params = [arg.arg for arg in node.args.args]
        header = f"function {node.name}({', '.join(params)}) " + "{"
        self.js_lines.append(header)
        self.indent_level += 1

        # Process the function body.
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1
        self.js_lines.append("}")

    # === Return Statement ===
    def visit_Return(self, node: ast.Return):  # noqa: N802
        ret_val = "" if node.value is None else self.visit(node.value)
        self.js_lines.append(f"{self.indent()}return {ret_val};")

    # === Expression Statements ===
    def visit_Expr(self, node: ast.Expr):  # noqa: N802
        # For standalone expressions, output them followed by a semicolon.
        expr = self.visit(node.value)
        self.js_lines.append(f"{self.indent()}{expr};")

    # === Assignment ===
    def visit_Assign(self, node: ast.Assign):  # noqa: N802
        if len(node.targets) != 1:
            raise TranspilerError("Multiple assignment targets are not supported yet.")
        target = self.visit(node.targets[0])
        value = self.visit(node.value)

        # Only use 'let' for new variable declarations (Name nodes)
        # Skip 'let' for subscript assignments and reassignments
        if (
            isinstance(node.targets[0], ast.Name)
            and node.targets[0].id not in self.declared_vars
        ):
            self.declared_vars.add(node.targets[0].id)
            self.js_lines.append(f"{self.indent()}let {target} = {value};")
        else:
            self.js_lines.append(f"{self.indent()}{target} = {value};")

    # === Binary Operations ===
    def visit_BinOp(self, node: ast.BinOp):  # noqa: N802
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = self.visit(node.op)
        return f"({left} {op} {right})"

    def visit_Add(self, node: ast.Add):  # noqa: N802, ARG002
        return "+"

    def visit_Sub(self, node: ast.Sub):  # noqa: N802, ARG002
        return "-"

    def visit_Mult(self, node: ast.Mult):  # noqa: N802, ARG002
        return "*"

    def visit_Div(self, node: ast.Div):  # noqa: N802, ARG002
        return "/"

    # === Comparison Operations ===
    def visit_Compare(self, node: ast.Compare):  # noqa: N802
        left = self.visit(node.left)
        ops = [self.visit(op) for op in node.ops]
        comparators = [self.visit(comp) for comp in node.comparators]

        # For now, we only support single comparisons
        if len(ops) != 1 or len(comparators) != 1:
            raise TranspilerError("Only single comparisons are supported")

        return f"({left} {ops[0]} {comparators[0]})"

    def visit_Gt(self, node: ast.Gt):  # noqa: N802, ARG002
        return ">"

    def visit_Lt(self, node: ast.Lt):  # noqa: N802, ARG002
        return "<"

    def visit_GtE(self, node: ast.GtE):  # noqa: N802, ARG002
        return ">="

    def visit_LtE(self, node: ast.LtE):  # noqa: N802, ARG002
        return "<="

    def visit_Eq(self, node: ast.Eq):  # noqa: N802, ARG002
        return "==="

    def visit_NotEq(self, node: ast.NotEq):  # noqa: N802, ARG002
        return "!=="

    # === If Statement ===
    def visit_If(self, node: ast.If):  # noqa: N802
        test = self.visit(node.test)
        self.js_lines.append(f"{self.indent()}if ({test}) " + "{")
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1
        self.js_lines.append(f"{self.indent()}" + "}")

        # Handle elif and else clauses
        current = node
        while (
            current.orelse
            and len(current.orelse) == 1
            and isinstance(current.orelse[0], ast.If)
        ):
            current = current.orelse[0]
            test = self.visit(current.test)
            self.js_lines.append(f"{self.indent()}else if ({test}) " + "{")
            self.indent_level += 1
            for stmt in current.body:
                self.visit(stmt)
            self.indent_level -= 1
            self.js_lines.append(f"{self.indent()}" + "}")

        # Handle final else clause if it exists
        if current.orelse:
            self.js_lines.append(f"{self.indent()}else " + "{")
            self.indent_level += 1
            for stmt in current.orelse:
                self.visit(stmt)
            self.indent_level -= 1
            self.js_lines.append(f"{self.indent()}" + "}")

    # === Function Calls ===
    def visit_Call(self, node: ast.Call):  # noqa: N802
        func = self.visit(node.func)
        args = [self.visit(arg) for arg in node.args]
        return f"{func}({', '.join(args)})"

    # === Variable Name ===
    def visit_Name(self, node: ast.Name):  # noqa: N802
        return node.id

    # === Constants ===
    def visit_Constant(self, node: ast.Constant):  # noqa: N802
        # Use repr() to generate a JS-friendly literal.
        return repr(node.value)

    # === For Loop ===
    def visit_For(self, node: ast.For):  # noqa: N802
        # Python: for i in range(10)
        # JavaScript: for (let i = 0; i < 10; i++)
        # or
        # Python: for item in items
        # JavaScript: for (let item of items)
        target = self.visit(node.target)
        iter_expr = self.visit(node.iter)

        # Special case for range()
        if (
            isinstance(node.iter, ast.Call)
            and isinstance(node.iter.func, ast.Name)
            and node.iter.func.id == "range"
        ):
            args = node.iter.args
            if len(args) == 1:  # range(stop)
                stop = self.visit(args[0])
                self.js_lines.append(
                    f"{self.indent()}for (let {target} = 0; {target} < {stop}; {target}++) "
                    + "{"
                )
            elif len(args) == 2:  # range(start, stop)
                start = self.visit(args[0])
                stop = self.visit(args[1])
                self.js_lines.append(
                    f"{self.indent()}for (let {target} = {start}; {target} < {stop}; {target}++) "
                    + "{"
                )
        else:
            # Generic for-of loop
            self.js_lines.append(
                f"{self.indent()}for (let {target} of {iter_expr}) " + "{"
            )

        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1
        self.js_lines.append(f"{self.indent()}" + "}")

    # === While Loop ===
    def visit_While(self, node: ast.While):  # noqa: N802
        test = self.visit(node.test)
        self.js_lines.append(f"{self.indent()}while ({test}) " + "{")
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1
        self.js_lines.append(f"{self.indent()}" + "}")

    # === List ===
    def visit_List(self, node: ast.List):  # noqa: N802
        elements = [self.visit(elt) for elt in node.elts]
        return f"[{', '.join(elements)}]"

    # === Subscript ===
    def visit_Subscript(self, node: ast.Subscript):  # noqa: N802
        value = self.visit(node.value)
        slice_value = self.visit(node.slice)
        return f"{value}[{slice_value}]"

    # === Augmented Assignment ===
    def visit_AugAssign(self, node: ast.AugAssign):  # noqa: N802
        target = self.visit(node.target)
        op = self.visit(node.op).strip()
        value = self.visit(node.value)
        self.js_lines.append(f"{self.indent()}{target} {op}= {value};")

    # === Boolean Operations ===
    def visit_BoolOp(self, node: ast.BoolOp):  # noqa: N802
        op = self.visit(node.op)
        values = [self.visit(value) for value in node.values]
        return f"({' ' + op + ' '.join(values)})"

    def visit_And(self, node: ast.And):  # noqa: N802, ARG002
        return "&&"

    def visit_Or(self, node: ast.Or):  # noqa: N802, ARG002
        return "||"

    # === Dictionary ===
    def visit_Dict(self, node: ast.Dict):  # noqa: N802
        pairs = []
        for key, value in zip(node.keys, node.values):
            if key is None:  # Handle dict unpacking
                continue
            key_js = self.visit(key)
            value_js = self.visit(value)
            pairs.append(f"{key_js}: {value_js}")
        return f"{{{', '.join(pairs)}}}"

    # === Fallback for Unsupported Nodes ===
    def generic_visit(self, node):
        raise TranspilerError(
            f"Unsupported or ambiguous syntax encountered: {ast.dump(node)}", node
        )


def transpile(fn: Callable) -> str:
    """
    Transpiles a Python function to JavaScript and returns the JavaScript code as a string.
    """
    try:
        source = inspect.getsource(fn)
        source = textwrap.dedent(source)
    except Exception as e:
        raise TranspilerError(
            "Could not retrieve source code from the function."
        ) from e

    # Parse the source code into an AST.
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        raise TranspilerError("Could not parse function source.") from e

    # Find the first function definition in the AST.
    func_node = None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            func_node = node
            break

    if func_node is None:
        raise TranspilerError("No function definition found in the provided source.")

    # Visit the function node to generate JavaScript code.
    visitor = PythonToJSVisitor()
    visitor.visit(func_node)
    return "\n".join(visitor.js_lines)


# === Example Usage ===
def example_function(x, y):
    z = x + y
    if z > 10:
        return z
    else:
        return 0


if __name__ == "__main__":
    try:
        js_code = transpile(example_function)
        print("Generated JavaScript Code:")
        print(js_code)
    except TranspilerError as err:
        print("Transpilation failed:", err)
