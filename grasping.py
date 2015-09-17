

acscatair = {
    'AZ' :{
    '1':['{{ branch_code }}',(slice(69,72))],
    '2':['{{ saved_fen_uncomp }}',slice(59,68)]
    '3':['{{ date_comp }}',slice(14,20)],
    '4':['{{ mck_code }}',slice(8,14)],
    '5':['{{ filer_code }}',(slice(5,8)],
    '6':['{{ cbp_port_code }}',slice(1,5)],
},
    'BY':{
    '1':['{{ filer_code }}',slice(7,10)],
    '2':['{{ port_of_entry }}',slice(3,7)]

},
    '10':{
    'port_of_entry':['{{ port_of_entry }}',slice(3,7)],
    'est_entry_date':['{{ est_entry_date }}',slice(49,55)],
    'filer_code':['{{ filer_code }}',slice(58,61)],
    'first_saved_fen_comp':['{# saved_fen_comp={{ fen_comp }} #}',slice(62,70)]
},
    '20':{
    'import_date':['{{ import_date }}',slice(33,39)],
    'first_saved_legacy_file_no_short':['{# saved_legacy_file_no_short={{ legacy_file_no_short }} #}',slice(39,48)]
    'est_arrival_date':['{{ est_arrival_date }}',slice(65,71)]
},
    '30':{
    'prelim_stmt_date':['{{ prelim_stmt_date }}',slice(53,59)]
},
    '50':{
    'export_date':['{{ export_date }}',slice(70,76)]
}
}



import xml.etree.ElementTree as etree
import collections as c
doc = 'sample_for_test.xml'
parser = etree.XMLParser(encoding='utf-8')
testCase = etree.parse(doc, parser)
az = c.OrderedDict(sorted(acscatair.items(), key=lambda x: x[0][1]))


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
        ace_catair_lines = root.findall('./env:Body/wrap:load7501FromCatair/wrap:in/wrap:aceAdditionalDataRecords', namespaces = self.namespace)
        branch_code = root.find('./env:Body/wrap:load7501FromCatair/wrap:in/web:branch_code', namespaces = self.namespace)
        formal_entry_no = root.find('./env:Body/wrap:load7501FromCatair/wrap:in/web:formalEntryNo', namespaces = self.namespace)
        legacy_file_no = root.find('./env:Body/wrap:load7501FromCatair/wrap:in/web:legacyFileNo', namespaces = self.namespace)
        filercode = root.find('./env:Body/wrap:load7501FromCatair/wrap:in/web:filerCode', namespaces = self.namespace)
        return acs_catair_lines, ace_catair_lines, branch_code, formal_entry_no, legacy_file_no, filercode

    def deal_with_acs(self):
        parsed_acs = []
        root = self.testCase.getroot()
        acs_catair_lines = root.findall('./env:Body/wrap:load7501FromCatair/wrap:in/web:acsCatairRecords', namespaces = self.namespace)
        for line in acs_catair_lines:
            if line.text.startswith('A'):
                line = list(line.text)
                for repl in self.acs_line_values['AZ']: #this won't take the order it is supposed to. see if there is anything new in 3.0 that can deal with this. 
                    print self.acs_line_values['AZ'][repl][0]
                    line[self.acs_line_values['AZ'][repl][1]:self.acs_line_values['AZ'][repl][2]] = self.acs_line_values['AZ'][repl][0]
                string = ''.join(line)
                parsed_acs.append(string)





