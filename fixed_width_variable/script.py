from grasping_more import *
import json
from collections import OrderedDict
import os
import xml.etree.ElementTree as etree

sys_input = str(sys.argv[1])
sys_output = str(sys.argv[2])

cust_map = json.load(open(os.path.join('input','to_json.json')))
cust_map['namespace_usentry']
#also the json file should just be dumped and ordered by the line value, then reverse ordered by the slice (high -> low)

<<<<<<< HEAD
doc = os.path.join('input','TEST_ME.xml')
=======
doc = os.path.join('input','%s.xml' % sys_input)
>>>>>>> 7b95eec77a5b218c730d4a55419b3807b7d3a950


parser = etree.XMLParser(encoding='utf-8')
testCase = etree.parse(doc, parser)

test = ReplaceItAll(testCase,cust_map['namespace'],cust_map)
test.register_ns()
test.ReplaceEverything(cust_map)
test.rewrite_TestCase(os.path.join('outputs','%s.xml' % sys_output))
