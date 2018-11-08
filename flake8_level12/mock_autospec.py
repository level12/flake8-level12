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

    def check_node(self, node):
        max_args = 1

        # make sure the decorator is a patch call
        if not isinstance(node, ast.Call):
            return
        if isinstance(node.func, ast.Name) and node.func.id != 'patch':
            return
        elif isinstance(node.func, (ast.Attribute, ast.Call)) and node.func.attr != 'patch':
            has_patch = False
            for child in ast.iter_child_nodes(node.func):
                if getattr(child, 'id', getattr(child, 'attr', None)) == 'patch':
                    max_args = 2
                    has_patch = True
            if not (node.func.attr in ('object', 'multiple') and has_patch):
                return
        # if we have more than max_args, we're directly assigning a mock value
        if len(node.args) > max_args:
            return

        node_kwargs = {keyword.arg: keyword.value for keyword in node.keywords}

        # make sure the expected kwargs are in place
        def check_kwarg(kwarg, ignore_with_spec=False):
            if ignore_with_spec and 'spec' in node_kwargs:
                # if spec is provided, autospec/spec_set should not be required
                return
            elif kwarg not in node_kwargs:
                self.add_error('{}_missing'.format(kwarg), node.lineno)
            elif not (
                isinstance(node_kwargs[kwarg], ast.NameConstant) and
                node_kwargs[kwarg].value is True
            ):
                self.add_error('{}_wrong'.format(kwarg), node.lineno)
        check_kwarg('autospec', ignore_with_spec=True)
        check_kwarg('spec_set')

    def run(self):
        for node in ast.walk(self.tree):
            if hasattr(node, 'decorator_list'):
                for decorator in node.decorator_list:
                    self.check_node(decorator)
            if isinstance(node, ast.withitem):
                self.check_node(node.context_expr)

        # linters are generators
        for error in self.errors:
            yield (error.get('line'), 0, error.get('message'), type(self))
