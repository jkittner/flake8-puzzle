import ast
import importlib.metadata as importlib_metadata
from typing import Any
from typing import Generator
from typing import List
from typing import Tuple
from typing import Type

MSG = 'PUZ6969 solved the puzzle!'


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.assignments: List[Tuple[int, int]] = []

    def visit_Call(self, node: ast.Call) -> None:
        if (
                isinstance(node, ast.Call) and
                node.args and
                not node.keywords and
                len(node.args) == 1 and
                isinstance(node.args[0], ast.Constant) and
                isinstance(node.args[0].value, str)
        ):
            self.assignments.append((node.lineno, node.col_offset))
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)
        for line, col in visitor.assignments:
            yield line, col, MSG, type(self)
