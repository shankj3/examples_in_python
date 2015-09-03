
#possibly a way to replace elements in a tag, say if the requirements are changed or if there are changes to data output (like from CDATA to be diffed as a string to xml for the edoc info)
import xml.etree.ElementTree as etree

#todo: replace this, it sucks. 

#xml_doc = input('Enter XML Document (w/o extension):')
#doc = '%s.xml' %(xml_doc)
#replacee = str(input('Whatchu tryna replace? :'))
#replacer = str(input('Whatchu tryna replace it with?:'))
#unique = str(input('What makes this element unique?:'))
tag = str(input('What\'s yo tag\'s name (with its namespace)?:')) 



namespaces = {"wrap": "urn:com:expd:customs:us_entry:servicewrappers",
                "sec":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd", 
                "util":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd", 
                "env":"http://schemas.xmlsoap.org/soap/envelope/", 
                "web":"urn:com:expd:customs:us_entry:webservices",
                "resp":"urn:expd.com:arch:core:response",
                "aphis":"urn:com:expd:customs:us:reports:aphis:lacey"}
def orginal_namespaces(tag, namespaces):
    for key in namespaces:
        if key+':' in tag:
            tag = tag.replace('%s:' %key,'{%s}' %namespaces[key])
    return tag
print(orginal_namespaces(tag, namespaces))

'''
parser = etree.XMLParser(encoding='utf-8')
testCase = etree.parse(doc,parser)
xml_root = testCase.getroot()
print(xml_root)

#tried to use root.find, but it doesn't like these namespaces or their expansion so I am officially confused... need to look into it 

#xmlns:aphis="urn:com:expd:customs:us:reports:aphis:lacey"
for prefix, uri in namespaces.items():
    etree.register_namespace(prefix,uri)

hi = []
for pg in xml_root.find('testRequest/testRequestHttpBody/env:Envelope/',namespaces):
    hi.append(pg.text)
print(hi)


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
for lineval in other_root.iter('{urn:com:expd:customs:us_entry:webservices}acsCatairRecords'):
    if lineval.text.startswith('PG01'):
        print(lineval.text)

'''
