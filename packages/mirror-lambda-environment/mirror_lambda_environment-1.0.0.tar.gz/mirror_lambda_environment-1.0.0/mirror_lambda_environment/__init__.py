from typing import Optional

import boto3
from inject_environment_variables import EnvironmentVariableInjector

from mirror_lambda_environment.utils import get_terminal_menu_selection


class MirrorLambdaEnvironment:
    def __init__(
        self,
        function_name: Optional[str] = None,
        prompt: Optional[bool] = False
    ):
        lambda_client = boto3.client('lambda')

        if function_name is None and prompt:
            functions: dict = lambda_client.list_functions(
                MaxItems=100
            )['Functions']
            function_names: list = [f['FunctionName'] for f in functions]
            function_name: str = function_names[
                get_terminal_menu_selection(function_names, 'Lambda Functions')
            ]

        if function_name:
            function: dict = lambda_client.get_function(FunctionName=function_name)
        else:
            raise Exception('Function name required')

        if function:
            function_variables: dict = function['Configuration']['Environment']['Variables']  # noqa: E501
            self.injector = EnvironmentVariableInjector(function_variables)
        else:
            raise Exception(f'Function {function_name} not found')

    def __enter__(self):
        self.injector.__enter__()

    def __exit__(self, *args):
        self.injector.__exit__()
