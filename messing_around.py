import grasping as g
def line_replacement(line,dictionary, key, parsed_line):
    for i in range(1, len(dictionary[key])+1):
        line[dictionary[key]['%s' %i][1]] = dictionary[key]['%s' %i][0]
    string = ''.join(line)
    parsed_line.append(string)

class ACS_Catair(ReplaceLines):
    def __init__(self, acs_line_values, dictionary):
        self.acs_line_values = acs_line_values

    def replace_acs(self):
        root = self.testCase.getroot()
        acs_catair_lines = root.findall('./testRequest/testRequestHttpBody/env:Envelope/env:Body/wrap:load7501FromCatair/wrap:in/web:acsCatairRecords', namespaces = self.namespace)
        for indi_line in acs_catair_lines:
            for key, value in acs_line_values.items():
                self.line_replacement(indi_line,acs_line_values,key)

#this method i think can be used to replace the redundancy in replace_acs_catair. 
def line_replacement(line,dictionary, key, parsed_section,lines_to_overwrite):
    for line in lines_to_overwrite:
            line = list(line.text)
        for i in range(1, len(dictionary[key])+1):
            if key = 'AZ' and line[0] == 'A' or line[0] =='Z': 
                line[dictionary[key]['%s' %i][1]] = dictionary[key]['%s' %i][0]
                string = ''.join(line)
                parsed_section.append(string)
            elif key = 'BY' and line[0] == 'B' or line[0] = 'Y':
                line[dictionary[key]['%s' %i][1]] = dictionary[key]['%s' %i][0]
                string = ''.join(line)
                parsed_section.append(string)
            elif line[0]+line[1] = key:
                line[dictionary[key]['%s' %i][1]] = dictionary[key]['%s' %i][0]
                string = ''.join(line)
                parsed_section.append(string)
            else:
                string = ''.join(line)
                parsed_section.append(string)

for key, val in g.acscatair.iteritems():
    print key

line_replacement('dkalsjdfalsdfkjadslfkjsl;dfjas',g.acscatair,)