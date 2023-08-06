[![Build Status](https://travis-ci.org/igordejanovic/parglare.svg?branch=master)](https://travis-ci.org/igordejanovic/parglare)
[![Coverage Status](https://coveralls.io/repos/github/igordejanovic/parglare/badge.svg?branch=master)](https://coveralls.io/github/igordejanovic/parglare?branch=master)
[![Docs](https://img.shields.io/badge/docs-latest-green.svg)](http://igordejanovic.net/parglare/)
![Status](https://img.shields.io/pypi/status/parglare.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python versions](https://img.shields.io/pypi/pyversions/parglare.svg)

![parglare logo](https://raw.githubusercontent.com/igordejanovic/parglare/master/docs/images/parglare-logo.png)

A pure Python LR/GLR parser with integrated scanner.


For more information see [the docs](http://www.igordejanovic.net/parglare/).


## Quick intro

This is just a small example to get the general idea. This example shows how to
parse and evaluate expressions with 5 operations with different priority and
associativity. Evaluation is done using semantic/reduction actions.

The whole expression evaluator is done in under 30 lines of code!

```python
from parglare import Parser, Grammar

grammar = r"""
E: E '+' E  {left, 1}
 | E '-' E  {left, 1}
 | E '*' E  {left, 2}
 | E '/' E  {left, 2}
 | E '^' E  {right, 3}
 | '(' E ')'
 | number;
number: /\d+(\.\d+)?/;
"""

actions = {
    "E": [lambda _, nodes: nodes[0] + nodes[2],
          lambda _, nodes: nodes[0] - nodes[2],
          lambda _, nodes: nodes[0] * nodes[2],
          lambda _, nodes: nodes[0] / nodes[2],
          lambda _, nodes: nodes[0] ** nodes[2],
          lambda _, nodes: nodes[1],
          lambda _, nodes: nodes[0]],
    "number": lambda _, value: float(value),
}

g = Grammar.from_string(grammar)
parser = Parser(g, debug=True, actions=actions)

result = parser.parse("34 + 4.6 / 2 * 4^2^2 + 78")

print("Result = ", result)

# Output
# -- Debuging/tracing output with detailed info about grammar, productions,
# -- terminals and nonterminals, DFA states, parsing progress,
# -- and at the end of the output:
# Result = 700.8
```

## Install

- Stable version:

    ```
    $ pip install parglare
    ```

- Development version:

    ```
    $ git clone git@github.com:igordejanovic/parglare.git
    $ pip install -e parglare
    ```


## License

MIT

## Python versions

Tested with 2.7, 3.3-3.6

## Credits

Initial layout/content of this package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
