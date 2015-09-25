acscatair = {
    'AZ' :{
    '1':['{{ branch_code }}',(slice(69,72))],
    '2':['{{ saved_fen_uncomp }}',(slice(59,68))],
    '3':['{{ date_comp }}',(slice(14,20))],
    '4':['{{ mck_code }}',(slice(8,14))],
    '5':['{{ filer_code }}',(slice(5,8))],
    '6':['{{ cbp_port_code }}',(slice(1,5))]
},
    'BY':{
    '1':['{{ filer_code }}',(slice(7,10))],
    '2':['{{ port_of_entry }}',(slice(3,7))]

},
    '10':{
    '4':['{{ port_of_entry }}',(slice(3,7))],
    '3':['{{ est_entry_date }}',(slice(49,55))],
    '2':['{{ filer_code }}',(slice(58,61))],
    '1':['{# saved_fen_comp={{ fen_comp }} #}',(slice(62,70))]
},
    '20':{
    '4':['{{ port_of_entry }}', (slice(29,33))],
    '3':['{{ import_date }}',(slice(33,39))],
    '2':['{# saved_legacy_file_no_short={{ legacy_file_no_short }} #}',(slice(39,48))],
    '1':['{{ est_arrival_date }}',(slice(65,71))]
},
    '30':{
    '1':['{{ prelim_stmt_date }}',(slice(53,59))],
#need to add stuff for 30, for certain entry types (31,32,34,38, and prob. more) need warehouse 
#filer cde, warehouse entry number which is actually a number from the test case before (the saved_fen_uncomp), 
},
    '50':{
    '1':['{{ export_date }}',(slice(70,76))]
}
}

ace_additional = {
    'TRLHDR': {
    '1':['{{ saved_fen_uncomp }}',(slice(6,15))],
    '2':['{{ filer_code }}',(slice(3,6))]
    }
}

#for aerecs, AZ and BY can be shared with acscatair.. prob. a better way to do this but not thinking about it rn.
aerecs = {
    'AZ' :{
    '1':['{{ branch_code }}',(slice(69,72))],
    '2':['{{ saved_fen_uncomp }}',(slice(59,68))],
    '3':['{{ date_comp }}',(slice(14,20))],
    '4':['{{ mck_code }}',(slice(8,14))],
    '5':['{{ filer_code }}',(slice(5,8))],
    '6':['{{ cbp_port_code }}',(slice(1,5))]
    },
    'BY':{
    '1':['{{ filer_code }}',(slice(7,10))],
    '2':['{{ port_of_entry }}',(slice(3,7))]
    },
    'SE10':{
    '3':['{{ filer_code }}',(slice(5,8))],
    '2':['{{ saved_fen_comp }}',(slice(10,18))],
    '1':['{{ port_of_entry }}',(slice(49,54))]
    },
    '10':{
    '1':['{{ prelim_stmt_date }}',(slice(51,57))],
    '2':['{{ saved_legacy_file_no_short }}',(slice(21,30))],
    '3':['{{ port_of_entry }}',(slice(17,21))],
    '4':['{{ saved_fen_comp }}',(slice(8,16))],
    '5':['{{ filer_code }}',(slice(3,6))]
    },
    '11':{
    '1':['{{ import_date }}',(slice(47,53))],
    '2':['{{ est_entry_date }}',(slice(41,47))]
    },
    '20':{
    '1':['{{ est_arrival_date }}',(slice(10,16))],
    },
    #SE16 (using ace_catair_entry_summary_create_update) says something about date of arrival, but not est.date of arrival. 
    #so not going to worry about it right now
    '40':{
    '1':['{{ export_date }}',(slice(12,18))]
    }
}
pgareports = {
    'initialsDate':'({{ report_date }})', #this one needs a slice of the original string. put it in there. 
    'branchName':'Expeditors {{ branch_code }}',
    'branchAddress':'{{ branch_address }}',
    'entryNo':'{{ filer_code }}-{{ saved_fen_uncomp }}',
    'anticipatedEP':'{{ port_of_entry }}'
}

request_body = {
    'branchCode':'{{ branch_code }}',
    'formalEntryNo':'{# saved_fen_uncomp={{ fen_uncomp }} #}',
    'legacyFileNo':'{# saved_legacy_file_no={{ legacy_file_no }} #}',
    'filerCode':'{{ filer_code }}'
}

request_header = {
    'REQUEST-LINE':'POST {{ usentry_endpoint }} HTTP/1.1',
    'ACCEPT-ENCODING':'gzip,deflate',
    'CONTENT-TYPE':'text/xml;charset=UTF-8',
    'SOAPACTION':'urn:com:expd:customs:us:servicewrappers/load7501FromCatair',
    'HOST':'{{ usentry_host }}:{{ usentry_port }}',
    'CONNECTION':'Keep-Alive',
    'USER-AGENT':'Apache-HttpClient/4.1.1 (java 1.5)'
}

namespace = {
    'wrap': 'urn:com:expd:customs:us:servicewrappers',
    'sec':'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd', 
    'util':'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd', 
    'env':'http://schemas.xmlsoap.org/soap/envelope/', 
    'web':'urn:com:expd:customs:us:webservices',
    'resp':'urn:expd.com:arch:core:response',
    'aphis':'urn:com:expd:customs:us:reports:aphis:lacey'
    }
