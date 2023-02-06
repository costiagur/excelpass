from bs4 import BeautifulSoup
import zipfile
import tempfile
import os
import json
from io import BytesIO

def returnpass(xlsxfile,jsonfile):

    tempf = tempfile.NamedTemporaryFile(mode="w+b",delete=False)

    tempf.write(xlsxfile)

    tempf.close()

    zippedxls = zipfile.ZipFile(tempf.name,mode="r")

    tempdir = tempfile.TemporaryDirectory()

    zippedxls.extractall(tempdir.name)

    zippedxls.close()
    seclog = json.load(BytesIO(jsonfile))

    for eachfilename in os.listdir(tempdir.name + '/xl/worksheets'):
        if eachfilename.find('xml') > -1:
            with open(tempdir.name + '/xl/worksheets/'+ eachfilename,mode="r+",encoding="utf8") as fp:
                soup = BeautifulSoup(fp, 'lxml-xml')
                if soup.find('sheetProtection') == None and seclog['/xl/worksheets/'+ eachfilename] != None:
                    newtag = soup.new_tag(seclog['/xl/worksheets/'+ eachfilename][1:-2])
                    soup.sheetData.insert_after(newtag)
                    fp.seek(0)
                    fp.write(str(soup))
                    fp.truncate()
                #
            #
        #
    #

    with open(tempdir.name + '/xl/workbook.xml',mode="r+",encoding="utf8") as wb:
        soupwb = BeautifulSoup(wb, 'lxml-xml')
        if soupwb.find('workbookProtection') == None and seclog['/xl/workbook.xml'] != None:
            newtag = soupwb.new_tag(seclog['/xl/workbook.xml'][1:-2])
            soupwb.bookViews.insert_before(newtag)
            wb.seek(0)
            wb.write(str(soupwb))
            wb.truncate()
        #
    #

    tempresf = tempfile.NamedTemporaryFile(mode="w+b",delete=False)

    zipres = zipfile.ZipFile(tempresf.name,mode="w")

    for upperdir, dirs, files in os.walk(top=tempdir.name):
        for eachfile in files:
            zipres.write(upperdir + "\\" + eachfile,arcname=upperdir.replace(tempdir.name,"")+"\\"+eachfile)  
        #
    #  

    zipres.close()

    tempresf.seek(0)

    resbites = tempresf.read()

    tempresf.close()
    tempdir.cleanup()
    os.unlink(tempf.name)

    return resbites
#
