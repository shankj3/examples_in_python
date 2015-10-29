
#possibly a way to replace elements in a tag, say if the requirements are changed or if there are changes to data output (like from CDATA to be diffed as a string to xml for the edoc info)
import xml.etree.ElementTree as etree
import os
#replace this, it sucks. 

#xml_doc = input('Enter XML Document (w/o extension):')
#doc = '%s.xml' %(xml_doc)
#replacee = str(input('Whatchu tryna replace? :'))
#replacer = str(input('Whatchu tryna replace it with?:'))
#unique = str(input('What makes this element unique?:'))
#tag = str(input('What\'s yo tag\'s name (with its namespace)?:')) 
'''


namespaces = {"wrap": "urn:com:expd:customs:us:servicewrappers","sec":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd", "util":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd", "env":"http://schemas.xmlsoap.org/soap/envelope/", "web":"urn:com:expd:customs:us:webservices","resp":"urn:expd.com:arch:core:response","aphis":"urn:com:expd:customs:us:reports:aphis:lacey"}
def orginal_namespaces(tag, namespaces):
    for key in namespaces:
        if key+':' in tag:
            tag = tag.replace('%s:' %key,'{%s}' %namespaces[key])
    return tag
print(orginal_namespaces(tag, namespaces))





parser = etree.XMLParser(encoding='utf-8')
testCase = etree.parse(doc,parser)
xml_root = testCase.getroot()
print(xml_root)

recs = root.findall('./testRequest/testRequestHttpBody/env:Envelope/env:Body/wrap:load7501FromCatair/wrap:in/web:acsCatairRecords', namespaces)

for prefix, uri in namespaces.items():
    etree.register_namespace(prefix,uri)


for lineval in xml_root.iter(tag):
    if lineval.text.startswith(unique):
        lineval.text = lineval.text.replace(replacee,replacer)
        print(lineval.text)
    testCase.write('check_it1.xml')

for lineval in xml_root.iter('{urn:com:expd:customs:us:reports:aphis:lacey}lineValue'):
    print(lineval.text)

parse1r = etree.XMLParser(encoding='utf-8')
othercases = etree.parse(doc,parse1r)

other_root = othercases.getroot()
for lineval in other_root.iter('{urn:com:expd:customs:us:webservices}acsCatairRecords'):
    if lineval.text.startswith('PG01'):
        print(lineval.text)



'''

def change_testid(doc, number):
    namespaces = {"wrap": "urn:com:expd:customs:us:servicewrappers","sec":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd", "util":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd", "env":"http://schemas.xmlsoap.org/soap/envelope/", "web":"urn:com:expd:customs:us:webservices","resp":"urn:expd.com:arch:core:response","aphis":"urn:com:expd:customs:us:reports:aphis:lacey"}
    parser = etree.XMLParser(encoding='utf-8')
    testCase = etree.parse(doc, parser)
    root = testCase.getroot()
    root.set('id',number)
    next = root.find('./testRequest/testRequestHttpBody/env:Envelope', namespaces)
    next.set('id',number)
#    testCase.write('CustomsWebServiceBranch_%s.xml'%number)
    print(next.attrib)
#change_testid('CustomsWebServiceBranch_015-024-0001.xml', '000-000-0000')


files = ['CustomsWebServiceBranch_015-0%s-0001.xml' %i for i in range(16,24,1)]
numbers =['015-0%02d-0001' %i for i in range(46,54,1)]

'''
if len(files)==len(numbers):
    for o,n in zip(files,numbers):
        change_testid(o,n)
else:
    print(len(files),len(numbers), numbers)
'''

def print_test_descrips():
    final = []
    for i in os.listdir(os.getcwd()):
        if i.endswith('.xml') and i.startswith('CustomsWebServiceBranch_'):
            parser = etree.XMLParser(encoding='utf-8')
            tests = etree.parse(i, parser)
            root = tests.getroot()
            descrip = root.find('./testMetadata/testDescription')
            author = root.find('./testMetadata/testCreateName')
#            final.append(str(root.attrib)+':'+descrip.text)
            with open('test_descriptions_20_Failing.txt','a') as f:
                f.write(str(root.attrib)+':'+author.text+' '+descrip.text)
                f.write('\n')
namespace= {
    "wrap": "urn:com:expd:customs:us:servicewrappers",
    "sec":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd", 
    "util":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd", 
    "env":"http://schemas.xmlsoap.org/soap/envelope/", 
    "web":"urn:com:expd:customs:us:webservices",
    "resp":"urn:expd.com:arch:core:response",
    "aphis":"urn:com:expd:customs:us:reports:aphis:lacey"
    }


namespace1= {
    "wrap": "urn:com:expd:customs:{{ usentry_ns }}:servicewrappers",
    "sec":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd", 
    "util":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd", 
    "env":"http://schemas.xmlsoap.org/soap/envelope/", 
    "web":"urn:com:expd:customs:{{ usentry_ns }}:webservices",
    "resp":"urn:expd.com:arch:core:response",
    "aphis":"urn:com:expd:customs:us:reports:aphis:lacey"
    }

namespace2= {
    "wrap": "urn:com:expd:customs:us_entry:servicewrappers",
    "sec":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd", 
    "util":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd", 
    "env":"http://schemas.xmlsoap.org/soap/envelope/", 
    "web":"urn:com:expd:customs:us_entry:webservices",
    "resp":"urn:expd.com:arch:core:response",
    "aphis":"urn:com:expd:customs:us:reports:aphis:lacey"
    }

def print_random_shit(fileno, doc=None):
    parser = etree.XMLParser(encoding='utf-8')
    tests = etree.parse('C:\\ext\dev\eclipse\CustomsWebServiceBranch\%s'% fileno, parser)
    root = tests.getroot()
    descrip = root.find('./testMetadata/testDescription')
    author = root.find('./testMetadata/testCreateName')
    acsCatairRecords = root.findall('./testRequest/testRequestHttpBody/env:Envelope/env:Body/wrap:load7501FromCatair/wrap:in/web:acsCatairRecords', namespace)
    alt_acsCatairRecords = root.findall('./testRequest/testRequestHttpBody/env:Envelope/env:Body/wrap:load7501FromCatair/wrap:in/web:acsCatairRecords', namespace1)
    altalt_acsCatairRecords = root.findall('./testRequest/testRequestHttpBody/env:Envelope/env:Body/wrap:load7501FromCatair/wrap:in/web:acsCatairRecords', namespace2)
#    hsnumbers = []
    if acsCatairRecords:
        return_hsnumbers_from_catair(acsCatairRecords,root,descrip)

    elif alt_acsCatairRecords:
        return_hsnumbers_from_catair(alt_acsCatairRecords,root,descrip)

    elif altalt_acsCatairRecords:
        return_hsnumbers_from_catair(altalt_acsCatairRecords,root,descrip)                     
    else:
        print(root.attrib['id'])
#                hsnumbers.append((str(i.text[3:13])))
#    return hsnumbers
import re

def return_hsnumbers_from_catair(lines,root, descrip):
    try:
        if descrip.text:
            try:
                for i in lines:
                    if i.text[0:2] in ['70','62','80','81']:
                        if i.text[2:12] != '          ':
                            with open('testdata_hsnumbers.txt', 'a') as f:
                                f.write('%s' % str(root.attrib['id']) +',,'+i.text[2:12] + ',,' + str(re.sub(r"\n", " ", descrip.text)))
                                f.write('\n')
#                        hsnumbers.append((str(i.text[2:12])))
#                        print(hsnumbers)
                    elif i.text[0:2] == '50':
                        if i.text[3:13] != '          ':
                            with open('testdata_hsnumbers.txt', 'a') as f:
                                f.write('%s' % str(root.attrib['id']) +',,'+i.text[3:13]+ ',,' + str(re.sub((r"\n"), " ", descrip.text)))
                                f.write('\n')       
            except UnicodeEncodeError:
                print('bad encode', root.attrib['id'])
        else:
            for i in lines:
                if i.text[0:2] in ['70','62','80','81']:
                    if i.text[2:12] != '          ':
                        with open('testdata_hsnumbers.txt', 'a') as f:
                            f.write('%s' % str(root.attrib['id']) +',,'+i.text[2:12]+ ',,')
                            f.write('\n')
#                    hsnumbers.append((str(i.text[2:12])))
#                    print(hsnumbers)
                elif i.text[0:2] == '50':
                    if i.text[3:13] != '          ':
                        with open('testdata_hsnumbers.txt', 'a') as f:
                            f.write('%s' % str(root.attrib['id']) +',,'+i.text[3:13]+ ',,')
                            f.write('\n')          
    except AttributeError:
        print('wtf', root.attrib['id'])
#     final.append(str(root.attrib)+':'+descrip.text)
#    if descrip.text:
#        if doc:
#            with open('test_descriptions_20_Failing.txt','a') as f:
#                f.write(str(root.attrib)+' --- '+author.text+' --- '+descrip.text)
#                f.write('\n')
#        else:
#            print(str(root.attrib), author.text, descrip.text)
#    else:
#        print(author.text,fileno)

a = ['015-0%s-0001' %i for i in range(80,85,1)]

def list_xmls_in_directory(path):
    xmls = []
    for files in os.listdir(path):
        if files[-3:] == 'xml':
            xmls.append(files)
    return xmls

customspath = 'C:/ext/dev/eclipse/CustomsWebServiceBranch'

for i in list_xmls_in_directory(customspath):
    print_random_shit(i)

#print(print_random_shit('CustomsWebServiceBranch_019-004-0001.xml'))

#def run_printshit(input):
#    for i in a:
#        print_random_shit(i)
#run_printshit(a)


#doc = 'variableinsert.xml'
parse1r = etree.XMLParser(encoding='utf-8')
#othercases = etree.parse(doc,parse1r)

def register():
    namespaces = {"wrap": "urn:com:expd:customs:us:servicewrappers","sec":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd", "util":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd", "env":"http://schemas.xmlsoap.org/soap/envelope/", "web":"urn:com:expd:customs:us:webservices","resp":"urn:expd.com:arch:core:response","aphis":"urn:com:expd:customs:us:reports:aphis:lacey"}
    for prefix, uri in namespaces.items():
        etree.register_namespace(prefix,uri)

def run_everything(line):
    import line_rules
    for i in dir(line_rules):
        item = getattr(line_rules,i)
        if callable(item):
            item(line)

def change_catair(doc):
    namespaces = {"wrap": "urn:com:expd:customs:us:servicewrappers","sec":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd", "util":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd", "env":"http://schemas.xmlsoap.org/soap/envelope/", "web":"urn:com:expd:customs:us:webservices","resp":"urn:expd.com:arch:core:response","aphis":"urn:com:expd:customs:us:reports:aphis:lacey"}
    register()
    parser = etree.XMLParser(encoding='utf-8')
    ex = etree.parse(doc, parser)
    root = ex.getroot()
    catair = root.findall('./{http://schemas.xmlsoap.org/soap/envelope/}Body/{urn:com:expd:customs:us:servicewrappers}load7501FromCatair/{urn:com:expd:customs:us:servicewrappers}in/{urn:com:expd:customs:us:webservices}acsCatairRecords', namespaces=namespaces)
    acecatair = root.findall('./env:Body/wrap:load7501FromCatair/wrap:in/web:aceAdditionalDataRecords', namespaces=namespaces)
    catairout = []
    for line in catair:
        catairout.append(line.text)
#    for a in acecatair:
#        catairout.append(a.text)
    return catairout
    #ex.write('variableinsert_out.xml')
#a = change_catair(doc)
#for i in a:
#    i = list(i)


def change_testid(doc, number):
    namespaces = {"wrap": "urn:com:expd:customs:us:servicewrappers","sec":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd", "env":"http://schemas.xmlsoap.org/soap/envelope/", "web":"urn:com:expd:customs:us:webservices"}
    for prefix, uri in namespaces.items():
        etree.register_namespace(prefix,uri)
    parser = etree.XMLParser(encoding='utf-8')
    testCase = etree.parse(doc, parser)
    root = testCase.getroot()
    root.set('id',number)
    next = root.find('./testRequest/testRequestHttpBody/env:Envelope', namespaces)
    next.set('id',number)
    testCase.write('CustomsWebServiceBranch_%s.xml'%number)
    print(next.attrib)
#change_testid('CustomsWebServiceBranch_015-100-1001.xml','015-100-1001')
number = ['015-0%s-0001' %i for i in range(80,87,1)]
docs = ['CustomsWebServiceBranch_001-001-900%s.xml' %i for i in range(1,8,1)]

def run_change_testid(D,N):
    if len(N) == len(D):
        for d,n in zip(D,N):
            change_testid(d,n)

#se11 = {'filercode':[1,5]}
#print(se11['filercode'][1])


def a_line(line):
    for indi in line:
        if indi.startswith('A'):
        #want to have this check against the varmap to make sure these slices exist there, way of making sure the fixed width is ok 
        #also if it is in the varmap, could you replace the number with the variable? that way if any variables change or something happens, would be able to accomodate that. 
#            individual = indi.replace(indi[d.A['cbp_port_code'][1]:d.A['cbp_port_code'][2]], d.A['cbp_port_code'][0]).replace(indi[d.A['filer_code'][1]:d.A['filer_code'][2]], d.A['filer_code'][0]).replace(indi[d.A['mck_code'][1]:d.A['mck_code'][2]], d.A['mck_code'][0]).replace(indi[d.A['date_comp'][1]:d.A['date_comp'][2]], d.A['date_comp'][0]).replace(indi[d.A['saved_fen_uncomp'][1]:d.A['saved_fen_uncomp'][2]], d.A['saved_fen_uncomp'][0]).replace(indi[d.A['branch_code'][1]:d.A['branch_code'][2]], d.A['branch_code'][0])
#            print(individual)
            list_indi = list(indi)
            list_indi[d.A['date_comp'][1]:d.A['date_comp'][2]] = d.A['date_comp'][0]
            list_indi[d.A['mck_code'][1]:d.A['mck_code'][2]] = d.A['mck_code'][0]
            list_indi[d.A['filer_code'][1]:d.A['filer_code'][2]] = d.A['filer_code'][0]
            list_indi[d.A['cbp_port_code'][1]:d.A['cbp_port_code'][2]] = d.A['cbp_port_code'][0]
            variabalized = ''.join(list_indi)
            print(variabalized)

def b_line(line):
    if line.text.startswith('B'):
        line.text = line.text[:2]+ 'asldfjk'


#import line_rules as d
import re


def replace(diction, st):
    for i,y in d.A.items(): 
        
        return newstr

