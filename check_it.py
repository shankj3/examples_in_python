<testCase id="015-014-0001" xmlns:env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:util="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" xmlns:wrap="urn:com:expd:customs:us:servicewrappers" xmlns:web="urn:com:expd:customs:us:webservices" xmlns:resp="urn:expd.com:arch:core:response" xmlns:def="urn:com:expd:customs:us:reports" xmlns:aphis="urn:com:expd:customs:us:reports:aphis:lacey" version="1.0">
	<testMetadata>
		<testCreateName>Jessi Shank</testCreateName>
		<testCreateDate>20150821</testCreateDate>
		<testDescription>generate APHIS report from ae transaction, also erase the phone number information of pg21 line, make sure report still looks correct. also change the HTS code in the 50 line, make sure that it doesn't affect report.Multiple states of origin</testDescription>
	</testMetadata>
	<testVariables>
		<testMaxTime>0</testMaxTime>
		<testDelay>0</testDelay>
		<testExecuteSqlQuery>false</testExecuteSqlQuery>
		<testSqlColumnsToIgnore/>
		<testSqlConnectionUrl/>
		<testSqlUsername/>
		<testSqlPassword/>
		<testSqlQueries/>
	</testVariables>
	<testRequest>
		<testRequestHttpHeader>
			<REQUEST-LINE>POST {{ usentry_endpoint }} HTTP/1.1</REQUEST-LINE>
			<ACCEPT-ENCODING>gzip,deflate</ACCEPT-ENCODING>
			<CONTENT-TYPE>text/xml;charset=UTF-8</CONTENT-TYPE>
			<SOAPACTION>urn:com:expd:customs:us:servicewrappers/load7501FromCatair</SOAPACTION>
			<CONTENT-LENGTH>4864</CONTENT-LENGTH>
			<HOST>{{ usentry_host }}:{{ usentry_port }}</HOST>
			<CONNECTION>Keep-Alive</CONNECTION>
			<USER-AGENT>Apache-HttpClient/4.1.1 (java 1.5)</USER-AGENT>
		</testRequestHttpHeader>
		<testRequestHttpBody>
			<env:Envelope id="015-014-0001">
				<env:Header>
					<sec:Security>
						<sec:UsernameToken web:Id="UsernameToken-1">
							<sec:Username>{{ usentry_sp_user }}</sec:Username>
							<sec:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{{ usentry_sp_pw }}</sec:Password>
						</sec:UsernameToken>
					</sec:Security>
				</env:Header>
				<env:Body>
					<wrap:load7501FromCatair>
						<wrap:in>
							<web:actionValues>
								<web:key>pgr</web:key>
								<web:values>
									<web:key>sendRequest</web:key>
									<web:value>true</web:value>
								</web:values>
								<web:values>
									<web:key>returnRequest</web:key>
									<web:value>true</web:value>
								</web:values>
							</web:actionValues>
							<web:branchCode>{{ branch_code }} </web:branchCode>
							<web:sendToCustoms>false</web:sendToCustoms>
							<web:sendSimplifiedEntry>false</web:sendSimplifiedEntry>
							<web:sendCensusOverrides>false</web:sendCensusOverrides>
							<web:returnAeRecs>true</web:returnAeRecs>
							<web:dutyCalculation>C</web:dutyCalculation>
							<web:feeCalculation>C</web:feeCalculation>

							<web:formalEntryNo>{# saved_fen_uncomp={{ fen_uncomp }} #}</web:formalEntryNo>
							<web:legacyFileNo>{# saved_legacy_file_no={{ legacy_file_no }} #}</web:legacyFileNo>
							<web:filerCode>{{ filer_code }}</web:filerCode>
							<web:acsCatairRecordCount>30</web:acsCatairRecordCount>
							<web:aceAdditionalDataRecordCount>23</web:aceAdditionalDataRecordCount>
							<web:acsCatairRecords>++PRIORITY CAR</web:acsCatairRecords>
							<web:acsCatairRecords>A3801{{ filer_code }}MCK001{{ date_comp }}01                                     {{ saved_fen_uncomp }} {{ branch_code }}5191</web:acsCatairRecords>
							<web:acsCatairRecords>B01{{ port_of_entry }}{{ filer_code }}EI                              19                         MW</web:acsCatairRecords>
							<web:acsCatairRecords>10A{{ port_of_entry }}91-10692480091-106924800                 8{{ est_entry_date }}   {{ filer_code }} {# saved_fen_comp={{ fen_comp }} #}01098  WA</web:acsCatairRecords>
							<web:acsCatairRecords>20                         403001{{ import_date }}{# saved_legacy_file_no_short={{ legacy_file_no_short }} #}19          6934 {{ est_arrival_date }}X187</web:acsCatairRecords>
							<web:acsCatairRecords>30                                  10              2{{ prelim_stmt_date }}             AA</web:acsCatairRecords>
							<web:acsCatairRecords>40001XO00000050000000005000                    0000000001               INV001</web:acsCatairRecords>
							<web:acsCatairRecords>50 4401210000          000000000000X                                CA{{ export_date }}N</web:acsCatairRecords>
							<web:acsCatairRecords>OI        FUEL WOOD, IN LOGS,ETC</web:acsCatairRecords>
							<web:acsCatairRecords>PG01001NHTMVS                                                                  A</web:acsCatairRecords>

							<web:acsCatairRecords>PG01002APHAPL</web:acsCatairRecords>
							<web:acsCatairRecords>PG02P</web:acsCatairRecords>
							<web:acsCatairRecords>PG10                   COMM DESC</web:acsCatairRecords>
							<web:acsCatairRecords>PG04 TEST ELEMENT                                       000000400000KG   0500000</web:acsCatairRecords>
							<web:acsCatairRecords>PG05GENUS NAME            SPECIES NAME</web:acsCatairRecords>
							<web:acsCatairRecords>PG06HRVCA</web:acsCatairRecords>
							<web:acsCatairRecords>PG06HRVWA</web:acsCatairRecords>
							<web:acsCatairRecords>PG06HRVOR</web:acsCatairRecords>
							<web:acsCatairRecords>PG06HRVNY</web:acsCatairRecords>
							<web:acsCatairRecords>PG06HRVAZ</web:acsCatairRecords>
							<web:acsCatairRecords>PG22             MF AP6 Y08242015</web:acsCatairRecords>
							<web:acsCatairRecords>PG21CI QA TESTER                             TEST@EMAIL.COM</web:acsCatairRecords>
							<web:acsCatairRecords>PG25                                                    000000005000</web:acsCatairRecords>
							<web:acsCatairRecords>PG01002EPAVNE                                                                  A</web:acsCatairRecords>

							<web:acsCatairRecords>60                                        XOALCFAB65RIC</web:acsCatairRecords>
							<web:acsCatairRecords>62          49900001732</web:acsCatairRecords>
							<web:acsCatairRecords>8949900000002500</web:acsCatairRecords>
							<web:acsCatairRecords>90                        00000000000000000000000000000250000000005000</web:acsCatairRecords>
							<web:acsCatairRecords>Y  {{ port_of_entry }}{{ filer_code }}EI00020                                                    MW</web:acsCatairRecords>
							<web:acsCatairRecords>Z3801{{ filer_code }}MCK001{{ date_comp }}01                                     {{ saved_fen_uncomp }} {{ branch_code }}5191</web:acsCatairRecords>
							<web:aceAdditionalDataRecords>HDR{{ filer_code }}{{ saved_fen_uncomp }}</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>ACM      8 XX 01MW                                                                                                                                             WA            ACE IMPORT PRERELEASE *DO NOT MODIF</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AM21238 Test BLVD                     Test Suite A56                     Laredo                             TX78045       08242015 00000025000000002500             NNNNN{{ saved_legacy_file_no }}00005000CTNS 00050000KXOALCFAB65RIC  08242015ABI</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AMOVNEN</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AMOODSN</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AMOFSIN</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AMONHTN</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AMOPSTN</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AMOTS1N</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AMOAPHY</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AMOFDAN</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AMOATFN</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AMODTCN</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AMOTTBN</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AMONMFN</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>ACI001 0000100000000USD0000000050000000000000500000</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AI2                                                                      0000000000000000000000000000N</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>ACL00010001                                       0000000000  0000000000   0000000000000000000000000000000000000000000      7 000000000000000000000000000000000000000</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AL2</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AEVDXR08242015</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AEVCSD09022015</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>AEVESF09042015</web:aceAdditionalDataRecords>
							<web:aceAdditionalDataRecords>TRL{{ filer_code }}{{ saved_fen_uncomp }}</web:aceAdditionalDataRecords>

						</wrap:in>
					</wrap:load7501FromCatair>
				</env:Body>
			</env:Envelope>
		</testRequestHttpBody>
	</testRequest>
	<testResponse>
		<testResponseHttpHeader>
			<STATUS-LINE>HTTP/1.1 200 OK</STATUS-LINE>
			<Date>Thu, 27 Feb 2014 21:26:46 GMT</Date>
			<Server>Apache/1.3.41 (Unix) mod_jk/1.2.26</Server>
			<Accept>text/xml, text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2</Accept>
			<SOAPAction>""</SOAPAction>
			<Content-Length>3638</Content-Length>
			<Keep-Alive>timeout=15, max=100</Keep-Alive>
			<Connection>Keep-Alive</Connection>
			<Content-Type>text/xml;charset=utf-8</Content-Type>
		</testResponseHttpHeader>
		<testResponseHttpBody>
			<env:Envelope>
				<env:Header/>
				<env:Body>
					<wrap:load7501FromCatairResponse>
						<wrap:out>
							<resp:hasConfirms>false</resp:hasConfirms>
							<resp:hasErrors>false</resp:hasErrors>
							<resp:hasMessages>true</resp:hasMessages>
							<resp:messages>
								<resp:severity>INFO</resp:severity>
								<resp:text>US Entry Duty matches CFIT Duty.</resp:text>
								<resp:category>GL05001</resp:category>
								<resp:number>5001</resp:number>
								<resp:fieldNames>dutyCalculation</resp:fieldNames>
							</resp:messages>
							<resp:messages>
								<resp:severity>INFO</resp:severity>
								<resp:text>US Entry Fees match CFIT Fees.</resp:text>
								<resp:category>GL05001</resp:category>
								<resp:number>5001</resp:number>
								<resp:fieldNames>feeCalculation</resp:fieldNames>
							</resp:messages>
							<web:usEntryVersion>{{ usentry_version }}</web:usEntryVersion>
							<web:aeRecs>
								<web:id>A</web:id>
								<web:aeData>A3801{{ filer_code }}MCK001{{ date_comp }}     AE                                {{ saved_fen_uncomp }} {{ branch_code }}5191   Y</web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>B</web:id>
								<web:aeData>B  {{ port_of_entry }}{{ filer_code }}AE                                                         MW         </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>10</web:id>
								<web:aeData>10A{{ filer_code }}  {{ saved_fen_comp }} {{ port_of_entry }}{{ saved_legacy_file_no_short }}   0140 X           2{{ prelim_stmt_date }}  19                   </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>11</web:id>
								<web:aeData>1191-10692480091-106924800               {{ est_entry_date }}{{ import_date }}       WA                  </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>20</web:id>
								<web:aeData>20AA  {{ port_of_entry }}{{ est_arrival_date }}X187                                                            </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>21</web:id>
								<web:aeData>216934                                                                          </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>31</web:id>
								<web:aeData>318B 098                                                                        </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>40</web:id>
								<web:aeData>40  001 XOCA{{ export_date }}        0000000001     0000005000    N                        </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>47</web:id>
								<web:aeData>47MXOALCFAB65RIC                                                                </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>47</web:id>
								<web:aeData>47C91-106924800                                                                 </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>47</web:id>
								<web:aeData>47S91-106924800                                                                 </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>50</web:id>
								<web:aeData>504401210000 0000000000 0000005000             X                                </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>OI</web:id>
								<web:aeData>OI        FUEL WOOD, IN LOGS,ETC                                                </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>PG</web:id>
								<web:aeData>PG01002APHAPL                                                                   </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>PG</web:id>
								<web:aeData>PG02P                                                                           </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>PG</web:id>
								<web:aeData>PG10                   COMM DESC                                                </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>PG</web:id>
								<web:aeData>PG04 TEST ELEMENT                                       000000400000KG   0500000</web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>PG</web:id>
								<web:aeData>PG05GENUS NAME            SPECIES NAME                                          </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>PG</web:id>
								<web:aeData>PG06HRVCA                                                                       </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>PG</web:id>
								<web:aeData>PG06HRVWA                                                                       </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>PG</web:id>
								<web:aeData>PG06HRVOR                                                                       </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>PG</web:id>
								<web:aeData>PG06HRVNY                                                                       </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>PG</web:id>
								<web:aeData>PG06HRVAZ                                                                       </web:aeData>
							</web:aeRecs>

							<web:aeRecs>
								<web:id>PG</web:id>
								<web:aeData>PG22             MF AP6 Y08242015                                               </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>PG</web:id>
								<web:aeData>PG21CI QA TESTER                             TEST@EMAIL.COM                     </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>PG</web:id>
								<web:aeData>PG25                                                    000000005000            </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>62</web:id>
								<web:aeData>6249900001732                                                                   </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>89</web:id>
								<web:aeData>8949900000002500                                                                </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>90</web:id>
								<web:aeData>9000000000000 00000002500 00000000000 00000000000 00000000000                   </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>Y</web:id>
								<web:aeData>Y  {{ port_of_entry }}{{ filer_code }}AE00027                                                               </web:aeData>
							</web:aeRecs>
							<web:aeRecs>
								<web:id>Z</web:id>
								<web:aeData>Z3801{{ filer_code }}MCK001{{ date_comp }}                                                            </web:aeData>
							</web:aeRecs>

							<web:actionValues>
								<web:key>PGR</web:key>
								<web:values>
									<web:key>returnRequest</web:key>
									<aphis:Lacey_Form>
										<aphis:initialsDate>MW ({{ report_date }})</aphis:initialsDate>
										<aphis:title>APHIS Lacey Act PGA Report</aphis:title>
										<aphis:branchName>Expeditors {{ branch_code }}</aphis:branchName>
										<aphis:branchAddress>{{ branch_address }}</aphis:branchAddress>
										<aphis:importerLabel>Importer: </aphis:importerLabel>
										<aphis:importer>ACE IMPORT PRERELEASE *DO NOT MODIF</aphis:importer>
										<aphis:entryNoLabel>Entry No. </aphis:entryNoLabel>
										<aphis:entryNo>{{ filer_code }}-{{ saved_fen_uncomp }}</aphis:entryNo>
										<aphis:importerNoLabel>Importer No. </aphis:importerNoLabel>
										<aphis:importerNo>91-106924800</aphis:importerNo>
										<aphis:anticipatedEPLabel>Anticipated Entry Port: </aphis:anticipatedEPLabel>
										<aphis:anticipatedEP>{{ port_of_entry }}</aphis:anticipatedEP>
										<aphis:invoiceLines>
											<aphis:invoiceLabel>7501 Line No:</aphis:invoiceLabel>
											<aphis:invoice>1</aphis:invoice>
											<aphis:lineLabel>PGA Line No:</aphis:lineLabel>
											<aphis:line>002</aphis:line>
											<aphis:commercialDescLabel>Commercial Description:</aphis:commercialDescLabel>
											<aphis:commercialDesc>FUEL WOOD, IN LOGS,ETC</aphis:commercialDesc>
											<aphis:commodityDescLabel>Product Description:</aphis:commodityDescLabel>
											<aphis:commodityDesc>COMM DESC</aphis:commodityDesc>
											<aphis:individualLabel>Certifying Individual:</aphis:individualLabel>
											<aphis:individual>QA TESTER</aphis:individual>
											<aphis:individualDetails>TEST@EMAIL.COM&#13;</aphis:individualDetails>
											<aphis:elementLabel>Element Name</aphis:elementLabel>
											<aphis:quantityLabel>Quantity</aphis:quantityLabel>
											<aphis:uomLabel>UOM</aphis:uomLabel>
											<aphis:recycledLabel>% Recycled</aphis:recycledLabel>
											<aphis:genusLabel>Genus and Species</aphis:genusLabel>
											<aphis:countryLabel>Country of Harvest</aphis:countryLabel>
											<aphis:elements>
												<aphis:element>TEST ELEMENT</aphis:element>
												<aphis:quantity>4,000</aphis:quantity>
												<aphis:uom>KG</aphis:uom>
												<aphis:recycled>50</aphis:recycled>
												<aphis:genus>GENUS NAME SPECIES NAME</aphis:genus>
												<aphis:country>CA, WA, OR, NY, AZ</aphis:country>
											</aphis:elements>
											<aphis:lineValue>Line Value (USD): 5,000.00</aphis:lineValue>
											<aphis:lineValue>Line Value (USD): 5,000.00</aphis:lineValue>
											<aphis:lineValue>Line Value (USD): 5,000.00</aphis:lineValue>
											<aphis:dateOfSignature>Date of Signature: 08-24-2015</aphis:dateOfSignature>
										</aphis:invoiceLines>
										<aphis:glossaryTitle>Glossary</aphis:glossaryTitle>
										<aphis:glossarySections>
											<def:definitionTitle>A1</def:definitionTitle>
											<def:definition>Phytosanitary certificate (Foreign)</def:definition>
										</aphis:glossarySections>
										<aphis:glossarySections>
											<def:definitionTitle>A10</def:definitionTitle>
											<def:definition>Permit to Move Live Plant Pests or Noxious Weeds</def:definition>
										</aphis:glossarySections>
										<aphis:glossarySections>
											<def:definitionTitle>A11</def:definitionTitle>
											<def:definition>Postentry Quarantine Permit (7CFR319.37-7)</def:definition>
										</aphis:glossarySections>
										<aphis:glossarySections>
											<def:definitionTitle>A12</def:definitionTitle>
											<def:definition>Permit to Import Timber or Timber Products</def:definition>
										</aphis:glossarySections>
										<aphis:glossarySections>
											<def:definitionTitle>A13</def:definitionTitle>
											<def:definition>Permit to Transit Plants and/or Plant Products, Plant Pests, and/or Associated Soil Through the United States</def:definition>
										</aphis:glossarySections>
										<aphis:glossarySections>
											<def:definitionTitle>A14</def:definitionTitle>
											<def:definition>Permit to Import Plants and Plant Products Regulated by 7CFR319.8 (Foreign Cotton or Covers)</def:definition>
										</aphis:glossarySections>
										<aphis:glossarySections>
											<def:definitionTitle>A15</def:definitionTitle>
											<def:definition>Permit to Import Plants and Plant Products Regulated by 7CFR319.15 (Sugarcane)</def:definition>
										</aphis:glossarySections>
										<aphis:glossarySections>
											<def:definitionTitle>A16</def:definitionTitle>
											<def:definition>Permit to Import Plants and Plant Products Regulated by 7CFR319.37 (Nursery Stock, Plants, Roots, Bulbs, Seeds)</def:definition>
										</aphis:glossarySections>
										<aphis:glossarySections>
											<def:definitionTitle>A17</def:definitionTitle>
											<def:definition>Permit to Import Plants and Plant Products Regulated by 7CFR319.41 (Indian Corn or Maize, Broomcorn, etc.)</def:definition>
										</aphis:glossarySections>
										<aphis:glossarySections>
											<def:definitionTitle>A18</def:definitionTitle>
											<def:definition>Permit to Import Plants and Plant Products Regulated by 7CFR319.55 (Rice)</def:definition>
										</aphis:glossarySections>
										<aphis:glossarySections>
											<def:definitionTitle>A19</def:definitionTitle>
											<def:definition>Permit to Import Plants and Plant Products Regulated by 7CFR319.56 (Fruits and Vegetables)</def:definition>
										</aphis:glossarySections>
										<aphis:glossarySections>
											<def:definitionTitle>A20</def:definitionTitle>
											<def:definition>Permit to Import Plants and Plant Products Regulated by 7CFR319.75 (Khapra Beetle)</def:definition>
										</aphis:glossarySections>
										<aphis:glossarySections>
											<def:definitionTitle>A21</def:definitionTitle>
											<def:definition>Permit to Import Plants and Plant Products Regulated by 7CFR319.37 (Canadian-Origin)</def:definition>
										</aphis:glossarySections>
										<aphis:glossarySections>
											<def:definitionTitle>A22</def:definitionTitle>
											<def:definition>Permit to Import Prohibited Plant Material For Research Purposes</def:definition>
										</aphis:glossarySections>
										<aphis:glossarySections>
											<def:definitionTitle>A23</def:definitionTitle>
											<def:definition>Protected Plant Permit to engage in the business of importing, exporting, or reexporting terrestrial plants regulated by 50CFR17.12 or 23.23 (Threatened or Endangered Species)</def:definition>
										</aphis:glossarySections>
										<aphis:glossarySections>
											<def:definitionTitle>FWD</def:definitionTitle>
											<def:definition>US CITES Document</def:definition>
										</aphis:glossarySections>
										<aphis:glossarySections>
											<def:definitionTitle>FWF</def:definitionTitle>
											<def:definition>Foreign CITES Document</def:definition>
										</aphis:glossarySections>
									</aphis:Lacey_Form>
								</web:values>
							</web:actionValues>
						</wrap:out>
					</wrap:load7501FromCatairResponse>
				</env:Body>
			</env:Envelope>
		</testResponseHttpBody>
	</testResponse>
</testCase>
