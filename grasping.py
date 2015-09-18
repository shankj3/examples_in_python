
import collections as c
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

import xml.etree.ElementTree as etree
import collections as c
doc = 'CustomsWebServiceBranch_002-001-0001.xml'
parser = etree.XMLParser(encoding='utf-8')
testCase = etree.parse(doc, parser)
az = c.OrderedDict(sorted(acscatair.iteritems(), key=lambda x: x[0][0]))

def line_replacement(line,dictionary, key, parsed_section, lines_to_overwrite):
    for i in range(1, len(dictionary[key])+1,1):
        line[dictionary[key]['%s' %i][1]] = dictionary[key]['%s' %i][0]
        string = ''.join(line)
        parsed_section.append(string)
    return parsed_section
    


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
    for prefix, uri in namespace.items():
        etree.register_namespace(prefix,uri)

    def get_necessary_lines(self): #this might not be that useful. 
        root = self.testCase.getroot()
        acs_catair_lines = root.findall('./env:Body/wrap:load7501FromCatair/wrap:in/web:acsCatairRecords', namespaces = self.namespace)
        ace_catair_lines = root.findall('./env:Body/wrap:load7501FromCatair/wrap:in/wrap:aceAdditionalDataRecords', namespaces = self.namespace)
        branch_code = root.find('./env:Body/wrap:load7501FromCatair/wrap:in/web:branch_code', namespaces = self.namespace)
        formal_entry_no = root.find('./env:Body/wrap:load7501FromCatair/wrap:in/web:formalEntryNo', namespaces = self.namespace)
        legacy_file_no = root.find('./env:Body/wrap:load7501FromCatair/wrap:in/web:legacyFileNo', namespaces = self.namespace)
        filercode = root.find('./env:Body/wrap:load7501FromCatair/wrap:in/web:filerCode', namespaces = self.namespace)
        return acs_catair_lines, ace_catair_lines, branch_code, formal_entry_no, legacy_file_no, filercode

    def replace_acs_catair(self):
        parsed_acs = []
        root = self.testCase.getroot()
        acs_catair_lines = root.findall('./testRequest/testRequestHttpBody/env:Envelope/env:Body/wrap:load7501FromCatair/wrap:in/web:acsCatairRecords', namespaces = self.namespace)
        if len(acs_catair_lines) == 0:
            print("etree didn't find any values. check paths/see if there are any variables in them.")
        for line in acs_catair_lines:
            line = list(line.text)
            if line[0] == 'A' or line[0] == 'Z':
                for i in range(1,7,1): # could make the range(1,len(dictionary)+1) then could be standardized across this shit
                    line[self.acs_line_values['AZ']['%s'%i][1]] = self.acs_line_values['AZ']['%s'%i][0]
                string = ''.join(line)
                parsed_acs.append(string)
            elif line[0] == 'B' or line[0] =='Y':
                for i in range(1,3,1):
                    line[self.acs_line_values['BY']['%s'%i][1]] = self.acs_line_values['BY']['%s'%i][0]
                string = ''.join(line)
                parsed_acs.append(string)
            elif line[0]+line[1] == '10':
                for i in range(1,5,1):
                    line[self.acs_line_values['10']['%s'%i][1]] = self.acs_line_values['10']['%s'%i][0]
                string = ''.join(line)
                parsed_acs.append(string)
            elif line[0]+line[1] == '20':
                for i in range(1,4,1):
                    line[self.acs_line_values['20']['%s'%i][1]] = self.acs_line_values['20']['%s'%i][0]
                string = ''.join(line)
                parsed_acs.append(string)
            elif line[0]+line[1] == '30':
                line[self.acs_line_values['30']['1'][1]] = self.acs_line_values['30']['1'][0]
                string = ''.join(line)
                parsed_acs.append(string)
            elif line[0]+line[1] == '50':
                line[self.acs_line_values['50']['1'][1]] = self.acs_line_values['50']['1'][0]
                string = ''.join(line)
                parsed_acs.append(string)
            else:
                string = ''.join(line)
                parsed_acs.append(string)
        for i,k in zip(acs_catair_lines,parsed_acs):
            i.text = k
    def try_replaceACS(self):
        parsed_acs = []
        root = self.testCase.getroot()
        acs_catair_lines = root.findall('./testRequest/testRequestHttpBody/env:Envelope/env:Body/wrap:load7501FromCatair/wrap:in/web:acsCatairRecords', namespaces = self.namespace)
        if len(acs_catair_lines) == 0:
            print("etree didn't find any values. check paths/see if there are any variables in them.")
        for line in acs_catair_lines:
            for keys, values in self.acs_line_values.iteritems():
                line_replacement(line,self.acs_line_values,keys,parsed_acs, acs_catair_lines)
        for i,k in zip(acs_catair_lines,line_replacement(line,self.acs_line_values,keys,parsed_acs, acs_catair_lines)):
            i.text = k
        for i in acs_catair_lines:
            print i.text
    def rewrite_TestCase(self):
        self.testCase.write('TEST_ME.xml')

class ACS(ReplaceLines):
    def __init__(self, testCase,acs_line_values):
        self.testCase = testCase
        self.acs_line_values = acs_line_values

class ACS_Catair(ReplaceLines):
    def __init__(self, acs_line_values, dictionary):
        self.acs_line_values = acs_line_values

    def replace_acs(self):
        root = self.testCase.getroot()
        acs_catair_lines = root.findall('./testRequest/testRequestHttpBody/env:Envelope/env:Body/wrap:load7501FromCatair/wrap:in/web:acsCatairRecords', namespaces = self.namespace)
        for indi_line in acs_catair_lines:
            for key, value in acs_line_values.items():
                self.line_replacement(indi_line,acs_line_values,key)

#a = ACS_Catair()
test = ReplaceLines(testCase,acscatair)
test.try_replaceACS()

