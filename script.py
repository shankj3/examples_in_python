from grasping_more import *
import json
from collections import OrderedDict

cust_map = json.load(open('to_json.json'),object_pairs_hook=OrderedDict)
doc = 'sample_classinheritance_customsweb.xml'
parser = etree.XMLParser(encoding='utf-8')
testCase = etree.parse(doc, parser)

test = ReplaceItAll(testCase,cust_map['namespace'],cust_map)
test.register_ns()
test.ReplaceEverything(cust_map)
test.rewrite_TestCase('sample_out_ordereddict.xml')

