import os

from copy import copy
from typing import Optional


class EnvironmentVariableInjector:
    def __init__(self, variables: dict):
        self.input_variables: dict = variables
        self.original_variables: Optional[dict] = None

    def __enter__(self):
        self.original_variables = copy(os.environ)
        new_environ = copy(os.environ)
        for k, v in self.input_variables.items():
            new_environ[k] = v
        os.environ = new_environ  # noqa: B003

    def __exit__(self, *args):
        if self.original_variables:
            os.environ = self.original_variables  # noqa: B003
