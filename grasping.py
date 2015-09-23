import xml.etree.ElementTree as etree
import collections as c
doc = 'CustomsWebServiceBranch_015-013-0007.xml'
parser = etree.XMLParser(encoding='utf-8')
testCase = etree.parse(doc, parser)
root = testCase.getroot()
#REALLY need to check against varmap, since when certain information isn't pertinetn, it won't show up on the line. 
# I guess though you could just have an if statment... if slice is empty don't fuck with it. 
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
    '4':['{{ port_of_entry }}', (slice(29,33))],
    '3':['{{ import_date }}',(slice(33,39))],
    '2':['{# saved_legacy_file_no_short={{ legacy_file_no_short }} #}',(slice(39,48))],
    '1':['{{ est_arrival_date }}',(slice(65,71))]
},
    '30':{
    '1':['{{ prelim_stmt_date }}',(slice(53,59))]
#need to add stuff for 30, for certain entry types (31,32,34,38, and prob. more) need warehouse 
#filer cde, warehouse entry number WHICH is actually a number from the test case before (the saved_fen_uncomp), 
},
    '50':{
    '1':['{{ export_date }}',(slice(70,76))]
}
}

ace_additional = {
    'TRLHDR': {
    '1':['{{ saved_fen_uncomp }}',(slice(6,15))],
    '2':['{{ filer_code }}',(slice(3,6))]
    }
}

#for aerecs, AZ and BY can be shared with acscatair.. prob. a better way to do this but not thinking about it rn.
aerecs = {
    'SE10':{
    '3':['{{ filer_code }}',(slice(5,8))],
    '2':['{{ saved_fen_comp }}',(slice(10,18))],
    '1':['{{ port_of_entry }}',(slice(49,54))]
    },
    '10':{
    '1':['{{ prelim_stmt_date }}',(slice(51,57))],
    '2':['{{ saved_legacy_file_no_short }}',(slice(21,30))],
    '3':['{{ port_of_entry }}',(slice(17,21))],
    '4':['{{ saved_fen_comp }}',(slice(8,16))],
    '5':['{{ filer_code }}',(slice(3,6))]
    },
    '11':{
    '1':['{{ import_date }}',(slice(47,53))],
    '2':['{{ est_entry_date }}',(slice(41,47))]
    },
    '20':{
    '1':['{{ est_arrival_date }}',(slice(10,16))],
    },
    #SE16 (using ace_catair_entry_summary_create_update) says something about date of arrival, but not est.date of arrival. 
    #so not going to worry about it right now
    '40':{
    '1':['{{ export_date }}',(slice(12,18))]
    }
}
pgareports = {
    'initialsDate':'({{ report_date }})', #this one needs a slice of the original string. put it in there. 
    'branchName':'Expeditors {{ branch_code }}',
    'branchAddress':'{{ branch_address }}',
    'entryNo':'{{ filer_code }}-{{ saved_fen_uncomp }}',
    'anticipatedEP':'{{ port_of_entry }}'
}

def stuff(dictionary,key,list_of_line,line):
    for i in range(1,len(dictionary[key])+1):
        if line.text[dictionary[key]['%s' %i][1]] == (' '*(len(line.text[dictionary[key]['%s' %i][1]]))):
            print(dictionary[key]['%s' %i][0],key,dictionary[key]['%s' %i][1])
        else:
            list_of_line[dictionary[key]['%s' %i][1]] = dictionary[key]['%s' %i][0]
    variabalized_string = ''.join(list_of_line)
    return variabalized_string

def line_replacement_by_section(line,dictionary): # add --> if the slice is empty, don't add things you shouldn't be. 
    listed_line = list(line.text)
    for key, values in dictionary.items():
        if key == 'AZ' and (line.text.startswith('A') or line.text.startswith('Z')): 
            string = stuff(dictionary,key,listed_line,line)
        elif key == 'BY' and (line.text.startswith('B') or line.text.startswith('Y')):
            string = stuff(dictionary,key,listed_line,line)
        elif key == 'TRLHDR' and(line.text.startswith('TRL') or line.text.startswith('HDR')):
            string = stuff(dictionary,key,listed_line,line)
        elif line.text.startswith(str(key)):
            string = stuff(dictionary,key,listed_line,line)
        else:
            string = ''.join(listed_line)
    return string
def register_ns(namespace):
    for prefix, uri in namespace.items():
        etree.register_namespace(prefix,uri)

class ReplaceLines(object):
    def __init__(self, testCase,acs_line_values,pga = None,aerecs_lines=None,aceadditional_lines=None): #just none for right now 
        self.testCase = testCase
        self.acs_line_values = acs_line_values
        self.aceadditional_lines = aceadditional_lines
        self.aerecs_lines = aerecs_lines
        self.pga = pga
    root = testCase.getroot()
    namespace = {
        "wrap": "urn:com:expd:customs:us_entry:servicewrappers",
        "sec":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd", 
        "util":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd", 
        "env":"http://schemas.xmlsoap.org/soap/envelope/", 
        "web":"urn:com:expd:customs:us_entry:webservices",
        "resp":"urn:expd.com:arch:core:response",
        "aphis":"urn:com:expd:customs:us:reports:aphis:lacey"
        }
    #issue: sometimes the namespaces are different (like :us: is :us_entry:), need to account for that
    register_ns(namespace)

    def try_replaceACS(self):
        parsed_acs = []
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
        return i.text
# these two between are waay too similar, need to fix that. 
    def try_replaceAErecs(self):
        parsed_ae = []
        aerecs = root.findall('./testResponse/testResponseHttpBody/env:Envelope/env:Body/wrap:load7501FromCatairResponse/wrap:out/web:aeRecs/web:aeData', namespaces = self.namespace)
        if len(aerecs) == 0:
            print("etree didn't find any values. check paths/see if there are any variables in them.")
        for ae in aerecs:
            parsed_ae.append(line_replacement_by_section(line,self.aerecs_lines))
        for i,k in zip(aerecs,parsed_ae):
            i.text = k
        return i.text

    def replace_PGA_reports(self):
        for keys, values in self.pga.items():
            replace_me = root.find('./testResponse/testResponseHttpBody/env:Envelope/env:Body/wrap:load7501FromCatairResponse/wrap:out/web:actionValues/web:values/aphis:Lacey_Form/aphis:%s'%(keys), namespaces = self.namespace)
            replace_me.text = values
        return replace_me.text

    def rewrite_TestCase(self):
        self.testCase.write('TEST_ME_aphis.xml')




test = ReplaceLines(testCase,acscatair,pgareports)
test.replace_PGA_reports()
#test.try_replaceAErecs()
test.rewrite_TestCase()
