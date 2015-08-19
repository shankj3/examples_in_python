'''
Identifiers

\d any number
\D anything but a number
\s space
\S anything but a space
\w any character
\W anything but a character
.  any character, except for a newline
\b the white space around words
\. a period

Modifiers: (amount, type etc)

{x,y} we're expecting x-y
+ Match 1 or more
? Match 0 or 1
* Match 0 or more
$ Match the end of a string
^ Match the beginning of string
| either or
[] range (variance) [A-Z] or [1-5a-qA-Z] (any of the following)
{x} expecting x amount

White Space Characters:
\n new line
\s space
\t tab
\e escape
\f form feed
\r return

DON'T FORGET!

. + * ? [ ] $ ^ ( ) { } | \ 

'''

import re

exampleString = '''
Jessica is 21 years old, and Daniel is 15 years old.
Edward is 97, and his grandfather, Oscar, is 102. 
'''
ages = re.findall(r'\d{1,3}', exampleString)
names = re.findall(r'[A-Z][a-z]*',exampleString)

print(ages)
print(names)


ageDict = {}
x = 0

for eachName in names: 
	ageDict[eachName] = ages[x]
	x+=1

print(ageDict)