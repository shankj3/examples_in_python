import xml.etree.ElementTree as etree
import collections as c
import current_map_customs as cust_map
import sys
import pprint


#varmap stuff, doesn't currently work. 
def varmap_stuff(varmap):
    lists = []
    with open('%s.varmap'%varmap,'r') as f:
        for line in f:
            lists.append(line.rstrip())
    return lists

def varmap_split(varmap_line):
    if '=' in str(varmap_line):
        variable, value = varmap_line.split('=', maxsplit = 1)
        return variable, value
    else:
        return None,None

def varmap_set_dictionary(varmap):
    varmap_dict = {}
    for line in varmap_stuff(varmap):
        one, two = varmap_split(line)
        varmap_dict.update({one:two})
    return varmap_dict 

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(varmap_set_dictionary('CustomsWebServiceBranch'))

#^^^ this as it is overwrites values because they have the same key ^^^

class ReplaceSections(object):
    def __init__(self, testCase,namespace): 
        self.testCase = testCase
        self.namespace = namespace
    #issue: sometimes the namespaces are different (like :us: is :us_entry:), need to account for that.. some kind of try or something. 

    def register_ns(self):
        for prefix, uri in self.namespace.items():
            etree.register_namespace(prefix,uri)

    def getroot(self):
        root = self.testCase.getroot()
        return root

    def string_replacement(self,dictionary,key,list_of_line,line):
        for i in range(1,len(dictionary[key])+1):
            if line.text[dictionary[key]['%s' %i][1]] == (' '*(len(line.text[dictionary[key]['%s' %i][1]]))):
                #with open('%s_unusedDictKeys.txt' %type(self.testCase).__name__,'a') as output:
                #    output.write(dictionary[key]['%s' %i][0] + ' ')
                #    output.write(key+' ')
                #    output.write(str(dictionary[key]['%s' %i][1]))
                #    output.write('\n')
                print(line.text[:3],dictionary[key]['%s' %i][0],str(dictionary[key]['%s' %i][1]))
            else:
                list_of_line[dictionary[key]['%s' %i][1]] = dictionary[key]['%s' %i][0]
        variabalized_string = ''.join(list_of_line)
        return variabalized_string

    def line_replacement_by_dictionary(self,line,dictionary):#iterates through dictionary on a specific line 
        listed_line = list(line.text)
        for key, values in dictionary.items():
            if key == 'AZ' and (line.text.startswith('A') or line.text.startswith('Z')): 
                string = self.string_replacement(dictionary,key,listed_line,line)
            elif key == 'BY' and (line.text.startswith('B') or line.text.startswith('Y')):
                string = self.string_replacement(dictionary,key,listed_line,line)
            elif key == 'TRLHDR' and(line.text.startswith('TRL') or line.text.startswith('HDR')):
                string = self.string_replacement(dictionary,key,listed_line,line)
            elif line.text.startswith(str(key)):
                string = self.string_replacement(dictionary,key,listed_line,line)
            else:
                string = ''.join(listed_line)
        return string

    def replace_chunks_in_XML(self,needed_xpath,dictionary):
        replaced_section = []
        original_chunk = self.getroot().findall(needed_xpath, namespaces = self.namespace)
        if len(original_chunk) == 0:
            print("didn't find any values. check paths/see if there are any variables in them.")
        for line in original_chunk:
            replaced_section.append(self.line_replacement_by_dictionary(line,dictionary))
        if len(replaced_section) != len(original_chunk):
            print('something went wrong, the output is not the same size as the input')
        else:
            for i, k in zip(original_chunk, replaced_section):
                i.text = k

    def replace_xml_tag_text(self, needed_xpath,dictionary):
        for keys, values in dictionary.items():
            try:
                original_tag = self.getroot().find('%s%s'%(needed_xpath, keys), namespaces = self.namespace)#my problem wtih this is xpath wont be exactly the same as ones for aerecs, etc. needs to be xpath/aphis:#key# which is weird
                original_tag.text = values
            except AttributeError:
                print('AttributeError:',sys.exc_info()[1],'\n Path is %s%s'%(needed_xpath, keys)) 

    def replace_requestHeader(self, dictionary):
        requestheader = self.getroot().findall('./testRequest/testRequestHttpHeader/')
        for entry in requestheader:
            if entry.tag in dictionary:
                entry.text = dictionary[entry.tag]

    def rewrite_TestCase(self,output):
        self.testCase.write(output)

class ReplaceItAll(ReplaceSections):
    def __init__(self, testCase,namespace):
        self.testCase = testCase
        self.namespace = namespace

    def ReplaceEverything(self):
        self.replace_chunks_in_XML('./testResponse/testResponseHttpBody/env:Envelope/env:Body/wrap:load7501FromCatairResponse/wrap:out/web:aeRecs/web:aeData',cust_map.aerecs)
        self.replace_chunks_in_XML('./testRequest/testRequestHttpBody/env:Envelope/env:Body/wrap:load7501FromCatair/wrap:in/web:aceAdditionalDataRecords',cust_map.ace_additional)
        self.replace_chunks_in_XML('./testRequest/testRequestHttpBody/env:Envelope/env:Body/wrap:load7501FromCatair/wrap:in/web:acsCatairRecords',cust_map.acscatair)
        self.replace_xml_tag_text('./testResponse/testResponseHttpBody/env:Envelope/env:Body/wrap:load7501FromCatairResponse/wrap:out/web:values/aphis:Lacey_Form/aphis:',cust_map.pgareports)
        self.replace_xml_tag_text('./testRequest/testRequestHttpBody/env:Envelope/env:Body/wrap:load7501FromCatair/wrap:in/web:',cust_map.request_body)
        self.replace_requestHeader(cust_map.request_header)

