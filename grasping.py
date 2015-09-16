acscatair = {
    'AZ' :{
    '1':['{{ branch_code }}',69,72],
    '2':['{{ saved_fen_uncomp }}',59,68],
    '3':['{{ date_comp }}',14,20],
    '4':['{{ mck_code }}',8,14],
    '5':['{{ filer_code }}',5,8],
    '6':['{{ cbp_port_code }}',1,5],
},
    'BY':{
    '1':['{{ filer_code }}',7,10],
    '2':['{{ port_of_entry }}',3,7]

},
    '10':{
    'port_of_entry':['{{ port_of_entry }}',3,7],
    'est_entry_date':['{{ est_entry_date }}',49,55],
    'filer_code':['{{ filer_code }}',58,61],
    'first_saved_fen_comp':['{# saved_fen_comp={{ fen_comp }} #}',62,70]
},
    '20':{
    'import_date':['{{ import_date }}',33,39],
    'first_saved_legacy_file_no_short':['{# saved_legacy_file_no_short={{ legacy_file_no_short }} #}',39,48],
    'est_arrival_date':['{{ est_arrival_date }}',65,71]
},
    '30':{
    'prelim_stmt_date':['{{ prelim_stmt_date }}',53,59]
},
    '50':{
    'export_date':['{{ export_date }}',70,76]
}
}
import xml.etree.ElementTree as etree
import collections as c
doc = 'sample_for_test.xml'
parser = etree.XMLParser(encoding='utf-8')
testCase = etree.parse(doc, parser)
az = c.OrderedDict(sorted(acscatair['AZ'].items(),key=lambda t: t[0]))

class ReplaceLines(object):
    def __init__(self, testCase,acs_line_values):
        self.testCase = testCase
        self.acs_line_values = acs_line_values
    namespace = {
        "wrap": "urn:com:expd:customs:us:servicewrappers",
        "sec":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd", 
        "util":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd", 
        "env":"http://schemas.xmlsoap.org/soap/envelope/", 
        "web":"urn:com:expd:customs:us:webservices",
        "resp":"urn:expd.com:arch:core:response",
        "aphis":"urn:com:expd:customs:us:reports:aphis:lacey"
        }
    def get_necessary_lines(self):
        root = self.testCase.getroot()
        acs_catair_lines = root.findall('./env:Body/wrap:load7501FromCatair/wrap:in/web:acsCatairRecords', namespaces = self.namespace)
    def tryit_(self):
        print(self.acs_catair_lines)

acs = ReplaceLines(testCase,acscatair)

