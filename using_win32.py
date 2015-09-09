
import win32com.client as win32
'''
word = win32.Dispatch("Word.Application")
word.Visible = 0
word.Documents.Open("MyDocument")
doc = word.ActiveDocument
To see how many tables your document has:

doc.Tables.Count
Then, you can select the table you want by its index. Note that, unlike python, COM indexing starts at 1:

table = doc.Tables(1)
To select a cell:

table.Cell(Row = 1, Column= 1)
To get its content:

table.Cell(Row =1, Column =1).Range.Text
Hope that this helps.

EDIT:

An example of a function that returns Column index based on its heading:

def Column_index(header_text):
for i in range(1 , table.Columns.Count+1):
    if table.Cell(Row = 1,Column = i).Range.Text == header_text:
        return i
then you can access the cell you want this way for example:

table.Cell(Row =1, Column = Column_index("The Column Header") ).Range.Text
'''
word = win32.Dispatch("Word.Application")
word.Visible = False
word.Documents.Open("Cargo Release_0.docx")
doc = word.ActiveDocument

table = doc.Tables(1)
a = table.Cell(Row=1,Column=1).Range.Text
AllTables = {}
for i in range(1,doc.Tables.Count - 1,1):
    table = doc.Tables(i)
    AllTables['Table%s'%i] = table
InputValues = {}
for key in AllTables:
#    print(AllTables[key].Cell(Row=1,Column=1).Range.Text)
    if "Input" in AllTables[key].Cell(Row=1,Column=1).Range.Text:
        InputValues[key] = AllTables[key]
#print(len(InputValues), len(AllTables))
