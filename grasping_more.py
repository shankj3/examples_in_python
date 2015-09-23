import xml.etree.ElementTree as etree
import collections as c
import current_map_customs as cust_map
doc = 'sample_classinheritance_customsweb.xml'
parser = etree.XMLParser(encoding='utf-8')
testCase = etree.parse(doc, parser)
#REALLY need to check against varmap, since when certain information isn't pertinetn, it won't show up on the line. 
# I guess though you could just have an if statment... if slice is empty don't fuck with it. 

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
    def __init__(self, testCase): #just none for right now 
        self.testCase = testCase

    root = testCase.getroot()
    namespace = {
        "wrap": "urn:com:expd:customs:us:servicewrappers",
        "sec":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd", 
        "util":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd", 
        "env":"http://schemas.xmlsoap.org/soap/envelope/", 
        "web":"urn:com:expd:customs:us:webservices",
        "resp":"urn:expd.com:arch:core:response",
        "aphis":"urn:com:expd:customs:us:reports:aphis:lacey"
        }
    #issue: sometimes the namespaces are different (like :us: is :us_entry:), need to account for that.. some kind of try or something. 
    register_ns(namespace)

    def replaceinXML(self,needed_xpath,dictionary):
        replaced_section = []
        original_chunk = self.root.findall(needed_xpath, namespaces = self.namespace)
        if len(original_chunk) == 0:
            print("didn't find any values. check paths/see if there are any variables in them.")
        for line in original_chunk:
            replaced_section.append(line_replacement_by_section(line,dictionary))
        if len(replaced_section) != len(original_chunk):
            print('something went wrong, the output is not the same size as the input!')
        else:
            for i, k in zip(original_chunk, replaced_section):
                i.text = k

    def rewrite_TestCase(self):
        self.testCase.write('sample_out.xml')

class ReplaceItAll(ReplaceLines):
    def __init__(self, testCase,acs_line_values=None,pga = None,aerecs_lines=None,aceadditional_lines=None, replaced_section = None): #just none for right now 
        self.replaced_section = replaced_section
        self.testCase = testCase
        self.acs_line_values = acs_line_values
        self.aceadditional_lines = aceadditional_lines
        self.aerecs_lines = aerecs_lines
        self.pga = pga
    def ReplaceEverything(self):
        self.replaceinXML('./testResponse/testResponseHttpBody/env:Envelope/env:Body/wrap:load7501FromCatairResponse/wrap:out/web:aeRecs/web:aeData',cust_map.aerecs)
        self.replaceinXML('./testRequest/testRequestHttpBody/env:Envelope/env:Body/wrap:load7501FromCatair/wrap:in/web:acsCatairRecords',cust_map.acscatair)
