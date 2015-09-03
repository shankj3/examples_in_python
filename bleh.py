with open('input.txt') as f:
    content = f.readlines()
with open('output.txt','w') as o:
    for i in content:
        i = i.replace('\n','')
        i = '<web:acsCatairRecords>%s</web:acsCatairRecords>' %i
        o.write(i)
        o.write('\n')
