from grasping_more import *
import json
from collections import OrderedDict
import os

cust_map = json.load(open(os.path.join('input','to_json.json')))

#also the json file should just be dumped and ordered by the line value, then reverse ordered by the slice (high -> low)

doc = os.path.join('input','TEST_ME.xml')


parser = etree.XMLParser(encoding='utf-8')
testCase = etree.parse(doc, parser)

test = ReplaceItAll(testCase,cust_map['namespace'],cust_map)
test.register_ns()
test.ReplaceEverything(cust_map)
test.rewrite_TestCase(os.path.join('outputs','pga_ttb.xml'))
