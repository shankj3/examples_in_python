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
    if '=' in str(varmap_leine):
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

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(varmap_set_dictionary('CustomsWebServiceBranch'))

#^^^ this as it is overwrites values because they have the same key ^^^

class ReplaceSections(object):
    def __init__(self, testCase,namespace,mapper): 
        self.testCase = testCase
        self.namespace = namespace
        self.mapper = mapper 
    #issue: sometimes the namespaces are different (like :us: is :us_entry:), need to account for that.. some kind of try or something. 

    def register_ns(self):
        for prefix, uri in self.namespace.items():
            etree.register_namespace(prefix,uri)

    def getroot(self):
        root = self.testCase.getroot()
        return root

    def string_replacement(self,dictionary,key,list_of_line,line):
        for replacee, slice_section in dictionary[key].items():
            if line.text[slice_section[0]:slice_section[1]] == (' '*(len(line.text[slice_section[0]:slice_section[1]]))):
                #with open('%s_unusedDictKeys.txt' %type(self.testCase).__name__,'a') as output:
                #    output.write(dictionary[key]['%s' %i][0] + ' ')
                #    output.write(key+' ')
                #    output.write(str(dictionary[key]['%s' %i][1]))
                #    output.write('\n')
                print(line.text[:3],replacee,slice_section)
            else:
                list_of_line[slice_section[0]:slice_section[1]] = str(replacee) 
        variabalized_string = ''.join(list_of_line)
        #print(variabalized_string)
        return variabalized_string

    def find_special_lines(self,entry):
        if entry[0] in ['A','Z']:
            identifier = 'AZ'
        elif entry[0] in ['B','Y']:
            identifier = 'BY'
        elif entry[:3] in ['TRL','HDR']:
            identifier = 'TRLHDR'
        else:
            identifier = str(entry[:2])
        print(identifier)
        return identifier


    def line_replacement_by_dictionary(self, line, dictionary):        
        listed_line = list(line.text)
        identifier = self.find_special_lines(line.text)
        if dictionary.get(identifier):
            new_line = self.string_replacement(dictionary, identifier, listed_line, line)
        else:
            new_line = line.text
        return new_line

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
    def __init__(self, testCase,namespace,mapper):
        self.testCase = testCase
        self.namespace = namespace
        self.mapper = mapper 

    def ReplaceEverything(self,mapper):
        self.replace_chunks_in_XML('./testResponse/testResponseHttpBody/env:Envelope/env:Body/wrap:load7501FromCatairResponse/wrap:out/web:aeRecs/web:aeData', mapper['aerecs'])
        self.replace_chunks_in_XML('./testRequest/testRequestHttpBody/env:Envelope/env:Body/wrap:load7501FromCatair/wrap:in/web:aceAdditionalDataRecords', mapper['ace_additional'])
        self.replace_chunks_in_XML('./testRequest/testRequestHttpBody/env:Envelope/env:Body/wrap:load7501FromCatair/wrap:in/web:acsCatairRecords', mapper['acscatair'])
        self.replace_xml_tag_text('./testResponse/testResponseHttpBody/env:Envelope/env:Body/wrap:load7501FromCatairResponse/wrap:out/web:values/aphis:Lacey_Form/aphis:', mapper['pgareports'])
        self.replace_xml_tag_text('./testRequest/testRequestHttpBody/env:Envelope/env:Body/wrap:load7501FromCatair/wrap:in/web:', mapper['request_body'])
        self.replace_requestHeader(mapper['request_header'])

