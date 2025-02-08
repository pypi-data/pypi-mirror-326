# Inject Environment Variables

A testing and development tool for temporarily injecting environment variables.

## Installation

```
pip install inject-environment-variables
```

## Usage

Variables can be injected into the environment via either a `with` statement or a decorator.

### With statement

Variables specified in the `EnvironmentVariableInjector`.

When the `with` exits the environment (`os.environ`) will be reset to how it was when the statement enters.
Meaning any changes to the environment during the statement will be lost.


```python
import os

from inject_environment_variables import EnvironmentVariableInjector

with EnvironmentVariableInjector({
  'VARIABLE_1': 'foo',
  'VARIABLE_2': 'bar'
}):
    print(os.getenv('VARIABLE_1')) 
```

### Decorator

Variables can be specified by decorating a function with the `inject_environment_variables` decorator.

These changes to the environment are only active for the duration of the decorated function. 
At the end of the function the environment will be reset to how it was when the function started, 
meaning any changes to the environment during the statement will be lost.

```python
import os

from inject_environment_variables.decorator import inject_environment_variables


@inject_environment_variables({
    'VARIABLE_1': 'foo',
    'VARIABLE_2': 'bar'
})
def test_environment_variables():
    print(os.getenv('VARIABLE_1')) 
```