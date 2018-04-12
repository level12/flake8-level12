import ast

from .version import version


ERROR_MESSAGES = {
    'autospec_missing': 'M100 autospec keyword arg missing',
    'autospec_wrong': 'M101 autospec keyword should be True',
    'spec_set_missing': 'M102 spec_set keyword arg missing',
    'spec_set_wrong': 'M103 spec_set keyword should be True',
}


class MockAutospecChecker(object):
    name = 'flake8-mock-autospec'
    version = version

    def __init__(self, tree):
        self.tree = tree
        self.errors = []

    def add_error(self, error, lineno):
        self.errors.append({
            'message': ERROR_MESSAGES[error],
            'line': lineno,
        })

    def run(self):
        def check_node(node):
            # make sure the decorator is a patch call
            if not isinstance(node, ast.Call):
                return
            if isinstance(node.func, ast.Name) and node.func.id != 'patch':
                return
            elif isinstance(node.func, (ast.Attribute, ast.Call)) and node.func.attr != 'patch':
                return
            # if we have more than one arg, we're directly assigning a mock value
            if len(node.args) > 1:
                return

            node_kwargs = {keyword.arg: keyword.value for keyword in node.keywords}

            # make sure the expected kwargs are in place
            def check_kwarg(kwarg):
                if kwarg not in node_kwargs:
                    self.add_error('{}_missing'.format(kwarg), node.lineno)
                elif not (
                    isinstance(node_kwargs[kwarg], ast.NameConstant) and
                    node_kwargs[kwarg].value is True
                ):
                    self.add_error('{}_wrong'.format(kwarg), node.lineno)
            check_kwarg('autospec')
            check_kwarg('spec_set')

        for node in ast.walk(self.tree):
            if hasattr(node, 'decorator_list'):
                for decorator in node.decorator_list:
                    check_node(decorator)
            if isinstance(node, ast.withitem):
                check_node(node.context_expr)

        # linters are generators
        for error in self.errors:
            yield (error.get('line'), 0, error.get('message'), type(self))
