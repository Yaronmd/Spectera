import pytest
import sys
import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../my_hook')))

from my_hook import spectra 

@spectra.attach("This is a passing teset.")
def test_pass():
    assert 1 == 1

def test_fail():
    assert 1 == 2

def test_skip():
    pytest.skip("Skipping this test")