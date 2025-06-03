import argparse

import pytest
import python_template
from python_template.__main__ import main, get_args_parser
import runpy


@pytest.mark.parametrize("dummy", list(range(10)))
def test_dummy(dummy):
    assert dummy < 10


@pytest.mark.parametrize(
    "attr",
    [
        "__author__",
        "__email__",
        "__copyright__",
        "__license__",
        "__url__",
        "__package__",
        "__version__",
    ],
)
def test_attributes(attr):
    assert hasattr(python_template, attr), f"Module does not have attribute {attr}"
    assert getattr(python_template, attr) is not None, f"Attribute {attr} is None"
    assert isinstance(
        getattr(python_template, attr), str
    ), f"Attribute {attr} is not a string"


def test_main():
    exit_code = main("")
    assert exit_code == 0, f"Main function did not return 0, got {exit_code}"


def test_get_args_parser():
    parser = get_args_parser()
    assert parser is not None, "get_args_parser returned None"
    assert isinstance(
        parser, argparse.ArgumentParser
    ), "get_args_parser did not return an ArgumentParser instance"
    # Check if the parser has the expected attributes
    assert hasattr(
        parser, "description"
    ), "ArgumentParser does not have a description attribute"
    assert (
        parser.description == "Python Template"
    ), "ArgumentParser description does not match expected value"
