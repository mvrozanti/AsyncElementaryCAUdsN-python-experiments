#!/usr/bin/env python
from aeca import *
import pytest
import sys

sync_priority = [1]*8

def test_normal_sync_on_async_context():
    for rule in range(255):
        spacetime_sync = run_sync(rule, 30, 30)
        spacetime_async = run_async(rule, 30, 30, sync_priority)
        assert spacetime_async == spacetime_sync

@pytest.mark.skipif(sys.maxsize < 0xffffffff, reason='Py_ssize_t too small for this test')
def test_for_conservative_rule_with_scheme():
    schemes = read_schemes_from_file('async-update-schemes.json')
    for rule in range(255):
        conservative = True
        for scheme in schemes:
            if not is_rule_conservative(rule, 30, 30, scheme):
                conservative = False
                break
        print('Rule', rule, 'is', '' if conservative else 'not', 'conservative')
