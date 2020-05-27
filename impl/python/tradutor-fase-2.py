#!/usr/bin/env python
import json
import code
import re
lines = open('ECAs e seus updates independentes-2.txt').read()
pairs = eval(lines.replace('{','[').replace('}',']').replace('_','1').replace('\n',''))
le_json = {}
for pair in pairs:
    rule = pair[1]
    _len = int(pair[3])
    schemes = pair[5]
    assert(_len == len(schemes))
    le_json[rule] = schemes
assert(len(le_json) == 16)
json.dump(le_json, open('updates_independentes_traduzidos-2.json', 'w'))
