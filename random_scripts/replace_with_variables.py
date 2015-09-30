import xml.etree.ElementTree as etree
import collections as c
doc = 'Sample_CustomsWebServiceBranch_XXX-XXX-XXXX.xml'
parser = etree.XMLParser(encoding='utf-8')
testCase = etree.parse(doc, parser)
root = testCase.getroot()

acscatair = {
    'AZ' :{
    '1':['{{ branch_code }}',(slice(69,72))],
    '2':['{{ saved_fen_uncomp }}',(slice(59,68))],
    '3':['{{ date_comp }}',(slice(14,20))],
    '4':['{{ mck_code }}',(slice(8,14))],
    '5':['{{ filer_code }}',(slice(5,8))],
    '6':['{{ cbp_port_code }}',(slice(1,5))]
},
    'BY':{
    '1':['{{ filer_code }}',(slice(7,10))],
    '2':['{{ port_of_entry }}',(slice(3,7))]

},
    '10':{
    '4':['{{ port_of_entry }}',(slice(3,7))],
    '3':['{{ est_entry_date }}',(slice(49,55))],
    '2':['{{ filer_code }}',(slice(58,61))],
    '1':['{# saved_fen_comp={{ fen_comp }} #}',(slice(62,70))]
},
    '20':{
    '3':['{{ import_date }}',(slice(33,39))],
    '2':['{# saved_legacy_file_no_short={{ legacy_file_no_short }} #}',(slice(39,48))],
    '1':['{{ est_arrival_date }}',(slice(65,71))]
},
    '30':{
    '1':['{{ prelim_stmt_date }}',(slice(53,59))]
},
    '50':{
    '1':['{{ export_date }}',(slice(70,76))]
}
}

def line_replacement_by_section(line,dictionary):
    line = list(line.text)
    for key, values in dictionary.items():
        if key == 'AZ' and (line[0] == 'A' or line[0] =='Z'): 
            for i in range(1, len(dictionary[key])+1):
                line[dictionary[key]['%s' %i][1]] = dictionary[key]['%s' %i][0]
            string = ''.join(line)
        elif key == 'BY' and (line[0] == 'B' or line[0] == 'Y'):
            for i in range(1, len(dictionary[key])+1):
                line[dictionary[key]['%s' %i][1]] = dictionary[key]['%s' %i][0]
            string = ''.join(line)
        elif line[0]+line[1] == str(key):
            for i in range(1, len(dictionary[key])+1):
                line[dictionary[key]['%s' %i][1]] = dictionary[key]['%s' %i][0]
            string = ''.join(line)
        else:
            string = ''.join(line)
    return string
def register_ns(namespace):
    for prefix, uri in namespace.items():
        etree.register_namespace(prefix,uri)

class ReplaceLines(object):
    def __init__(self, testCase,acs_line_values, aceadditional_lines=None, aerecs_lines=None): #just none for right now 
        self.testCase = testCase
        self.acs_line_values = acs_line_values
        self.aceadditional_lines = aceadditional_lines
        self.aerecs_lines = aerecs_lines

    namespace = {
        "wrap": "urn:com:expd:customs:us:servicewrappers",
        "sec":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd", 
        "util":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd", 
        "env":"http://schemas.xmlsoap.org/soap/envelope/", 
        "web":"urn:com:expd:customs:us:webservices",
        "resp":"urn:expd.com:arch:core:response",
        "aphis":"urn:com:expd:customs:us:reports:aphis:lacey"
        }
    register_ns(namespace)

    def try_replaceACS(self):
        parsed_acs = []
        root = self.testCase.getroot()
        acs_catair_lines = root.findall('./testRequest/testRequestHttpBody/env:Envelope/env:Body/wrap:load7501FromCatair/wrap:in/web:acsCatairRecords', namespaces = self.namespace)
        if len(acs_catair_lines) == 0:
            print("etree didn't find any values. check paths/see if there are any variables in them.")
        for line in acs_catair_lines:
            parsed_acs.append(line_replacement_by_section(line,self.acs_line_values))
        if len(parsed_acs) != len(acs_catair_lines):
            print('something went wrong, the output is not the same size as the input!')
        else:
            for i, k in zip(acs_catair_lines, parsed_acs):
                i.text = k

    def rewrite_TestCase(self):
        self.testCase.write('TEST_ME.xml')



test = ReplaceLines(testCase,acscatair)
test.try_replaceACS()
test.rewrite_TestCase()
