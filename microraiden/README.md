# Development

If you want to develop applications based on microraiden,
we provide you with a good starting point.

 - [Development documentation](
 https://microraiden.readthedocs.io/en/latest/index.html#development)
 - [Python API Documentation](
 https://microraiden.readthedocs.io/en/latest/api-reference.html)

Please be aware, that we didn't arrive at a final release yet,
so we don't guarantee that the API will stay consistent and
backwards-compatible.

Since we develop with a high pace, it may be possible that
the documentation is outdated. Whenever you find some inconsistencies,
please [help us](#contribution-guidelines) by reporting or fixing the documentation.

## Installation

For developing purposes you should install microraiden in pip's
`editable` mode:

```
git clone git@github.com:raiden-network/microraiden.git
cd microraiden/microraiden
pip install -r requirements-dev.txt
pip install -e .
```

Further instructions can be found in the [development documentation]().

## Contribution Guidelines

We are always happy about your contribution and support.
Whenever you encounter a problem, please feel free to file an issue
or even correct the problem yourself with a code contribution.

However, to make it easier for us to help you and verify your
contributions, please follow our guidelines:

### Filing Issues

Before creating an issue please make sure that you followed the
instructions in the documentation and that your system is
configured properly.
When you still have problems and decide to open an issue,
please be as specific as you can.
If you click on GitHub's `New issue`, we already prepared a template
issue for you. Please adhere to the structure that is given there.

<!--### Code style TODO-->

### Docstrings

For consistency and for auto-generating our API-Docs, we agreed on a
specific docstring-style.

We try to document our classes, methods and modules in the
[Google docstring style](
https://google.github.io/styleguide/pyguide.html?showone=Comments#Comments)


Since we are using Python 3, we also want to include
[type hints](https://docs.python.org/3.5/library/typing.html) in our code.

To avoid duplication of type annotions from the google style docstrings,
we leave out the types there.

Instead of
```
def function(foo: str, bar: int) -> int:
    """ Short description

    Long description

    Args:
        foo (str): some arg
        bar (int): another arg

    Returns:
        int: The number "1"
    """
    return 1
```

we would use:
```
def function(foo: str, bar: int) -> int:
    """ Short description

    Long description

    Args:
        foo: some arg
        bar: another arg

    Returns:
        The number "1"
    """
    return 1
```


### Code contributions

In order to contribute, you have to sign our
[CLA](https://cla-assistant.io/raiden-network/microraiden).


Whenever you want to fix an issue or contribute to our code,
please:
 - fork the microraiden repository
 - write your code
 - push to your fork
 - create a merge-pull-request (for now directly to the `master` branch)

In order to be mergeable, the PR needs a review by at least one of
our maintainers, and the tests on our CI mustn't fail.

Please tag the PR with the `please review` label.