import ast

from .version import version


ERROR_MESSAGES = {
    'precision_missing': 'M110 missing precision for numeric column',
    'scale_missing': 'M111 missing scale for numeric column',
}


class NumericPrecisionScaleChecker(ast.NodeVisitor):
    name = 'flake8-numeric-precision'
    version = version

    def __init__(self, tree):
        self.tree = tree
        self.errors = []
        self.sa_symbols = set()
        self.numeric_class_symbols = set()

    def add_error(self, error, lineno):
        self.errors.append({
            'message': ERROR_MESSAGES[error],
            'line': lineno,
        })

    def handle_import(self, node):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == 'sqlalchemy':
                    self.sa_symbols.add(alias.asname if alias.asname else alias.name)
        elif node.module == 'sqlalchemy':
            assert isinstance(node, ast.ImportFrom)
            for alias in node.names:
                if alias.name in ('Numeric', 'NUMERIC'):
                    self.numeric_class_symbols.add(alias.asname if alias.asname else alias.name)

    def gather_symbols(self):
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                self.handle_import(node)

    def visit_Attribute(self, node):
        if (
            isinstance(node.value, ast.Name) and
            node.value.id in self.sa_symbols and
            node.attr in ('Numeric', 'NUMERIC')
        ):
            self.check_numeric_call(node)
        else:
            self.generic_visit(node)

    def visit_Name(self, node):
        if node.id in self.numeric_class_symbols:
            self.check_numeric_call(node)
        else:
            self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.numeric_class_symbols:
                self.check_numeric_call(node)
                return
        elif isinstance(node.func, ast.Attribute):
            if (
                isinstance(node.func.value, ast.Name) and
                node.func.value.id in self.sa_symbols and
                node.func.attr in ('Numeric', 'NUMERIC')
            ):
                self.check_numeric_call(node)
                return
        self.generic_visit(node)

    def check_numeric_call(self, node):
        if not isinstance(node, ast.Call):
            self.add_error('precision_missing', node.lineno)
            self.add_error('scale_missing', node.lineno)
            return

        if len(node.args) >= 2:
            return

        precision_arg_found = False
        scale_arg_found = False

        if len(node.args) == 1:
            precision_arg_found = True

        for kwarg in node.keywords:
            if kwarg.arg == 'precision':
                precision_arg_found = True
            if kwarg.arg == 'scale':
                scale_arg_found = True

        if not precision_arg_found:
            self.add_error('precision_missing', node.lineno)
        if not scale_arg_found:
            self.add_error('scale_missing', node.lineno)

    def run(self):
        self.gather_symbols()

        self.visit(self.tree)

        # linters are generators
        for error in self.errors:
            yield (error.get('line'), 0, error.get('message'), type(self))
