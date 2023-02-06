# excelpass
The project removes limitations committed by user in XLSX and XLSM files. It removes security tag from the underlying XML file of each worksheet and the workbook. The tags are stored in json file and security can be restored afterwards.
The aim is to help user that forgot his/her password or to free Excel file for his normal use.
requires installation of Beatiful Soup and lxml parser:
$ pip install lxml
$ pip install beautifulsoup4
