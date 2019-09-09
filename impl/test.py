#!/usr/bin/env python
from aeca import *

sync_priority = (1,1,1,1,1,1,1,1)

def test_normal_sync_on_async_context():
    for rule in range(255):
        spacetime_sync = run_sync(rule, 30, 30)
        spacetime_async = run_async(rule, 30, 30, sync_priority)
        assert spacetime_async == spacetime_sync

