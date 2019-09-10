#!/usr/bin/env python
from aeca import *
import pytest
import sys
import unittest

sync_priority = [1]*8

def test_normal_sync_on_async_context():
    for rule in range(255):
        spacetime_sync = run_sync(rule, 30, 30)
        spacetime_async = run_async(rule, 30, 30, sync_priority)
        assert list(spacetime_async) == list(spacetime_sync)

# @pytest.mark.skipif(sys.maxsize < 0xffffffff, reason='Py_ssize_t too small for this test')
@unittest.skip("too costly")
def test_for_conservative_rule_with_scheme():
    w = t = 10
    schemes = read_schemes_from_file('async-update-schemes.json')
    for rule in range(1,255):
        for scheme in schemes:
            print('Rule', rule, 'is', '' if is_rule_conservative(rule, w, t, scheme) else 'not', 'conservative with scheme', scheme)

def test_for_conservative_rule_without_scheme():
    w = t = 10
    conservative_rules_in_sync_scheme_count = 0
    for rule in range(1,255):
        is_conservative = is_rule_conservative(rule, w, t)
        conservative_rules_in_sync_scheme_count += int(is_conservative)
        print('Rule', rule, 'is', '' if is_conservative else 'not', 'conservative')
    assert conservative_rules_in_sync_scheme_count == 5


if __name__ == '__main__':
    test_for_conservative_rule_with_scheme()
