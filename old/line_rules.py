
#acsCatairRecords Dictionary
A = {
    'cbp_port_code':['{{ cbp_port_code }}',1,5],
    'filer_code':['{{ filer_code }}',5,8],
    'mck_code':['{{ mck_code }}',8,14],
    'date_comp':['{{ date_comp }}',14,20],
    'saved_fen_uncomp':['{{ saved_fen_uncomp }}',59,68],
    'branch_code':['{{ branch_code }}',69,72]
}

B = {
    'port_of_entry':['{{ port_of_entry }}',3,7],
    'filer_code':['{{ filer_code }}',7,10]
}

_10 = {
    'port_of_entry':['{{ port_of_entry }}',3,7],
    'est_entry_date':['{{ est_entry_date }}',49,55],
    'filer_code':['{{ filer_code }}',58,61],
    'first_saved_fen_comp':['{# saved_fen_comp={{ fen_comp }} #}',62,70]
}

#port of entry in _20 line, technically port of unlading.. seems to still be 3001 across the board, but idk if 
#actually always port_of_entry
_20 = {
    'import_date':['{{ import_date }}',33,39],
    'first_saved_legacy_file_no_short':['{# saved_legacy_file_no_short={{ legacy_file_no_short }} #}',39,48],
    'est_arrival_date':['{{ est_arrival_date }}',65,71]
}

_30 = {
    'prelim_stmt_date':['{{ prelim_stmt_date }}',53,59]
    }

_50 = {
    'export_date':['{{ export_date }}',70,76]
}

Y = {
    'port_of_entry':['{{ port_of_entry }}',3,7],
    'filer_code':['{{ filer_code }}',7,10]
}

Z= {
    'cbp_port_code':['{{ cbp_port_code }}',1,5],
    'filer_code':['{{ filer_code }}',5,8],
    'mck_code':['{{ mck_code }}',8,14],
    'date_comp':['{{ date_comp }}',14,20],
    'saved_fen_uncomp':['{{ saved_fen_uncomp }}',59,68],
    'branch_code':['{{ branch_code }}',69,72]
}

'''
def a_line(line):
    if line.text.startswith('A'):
        #want to have this check against the varmap to make sure these slices exist there, way of making sure the fixed width is ok 
        #also if it is in the varmap, could you replace the number with the variable? that way if any variables change or something happens, would be able to accomodate that. 
        a = list(line.text)
        print(a)
#def b_line(line):
#    if line.text.startswith('B'):
#        line.text = line.text[:2]+ 'asldfjk'
print(A.keys())

line = 'A3027231MCK02209141501                                     0063617-3 CLT8218'
a_line(line)
'''
