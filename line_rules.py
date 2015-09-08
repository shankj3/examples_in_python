def a_line(line):
    if line.text.startswith('A'):
        #want to have this check against the varmap to make sure these slices exist there, way of making sure the fixed width is ok 
        #also if it is in the varmap, could you replace the number with the variable? that way if any variables change or something happens, would be able to accomodate that. 
        line.text = line.text[:5]+'{{ filer_code }}'+'{{ mck_code }}'+'{{ date_comp }}'+line.text[20:69]+'{{ branch_code }}'+line.text[72:]
        print(line.text)
#def b_line(line):
#    if line.text.startswith('B'):
#        line.text = line.text[:2]+ 'asldfjk'
