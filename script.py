from grasping_more import *
import current_map_customs as cust_map

doc = 'sample_classinheritance_customsweb.xml'
parser = etree.XMLParser(encoding='utf-8')
testCase = etree.parse(doc, parser)

test = ReplaceItAll(testCase,cust_map.namespace)
test.register_ns()
test.ReplaceEverything()
test.rewrite_TestCase('sample_out.xml')

