import base64
import json
import common
import removepass
import returnpass

CODESTR = "xlsxpass"

def myfunc(queryobj):
    #try:
        postdict = queryobj._POST()
        filesdict = queryobj._FILES()
        
        #print("POST = " + str(postdict) + "\n")
        #print("FILES = " + str(filesdict) + "\n")

        restuple = ""

        if postdict["action"] == "removepass":
            restuple = removepass.removepass(filesdict["xlsxfile"][1])
        
        elif postdict["action"] == "returnpass":
            res = returnpass.returnpass(filesdict["xlsxfile"][1], filesdict["jsonfile"][1])
        #
        # reply message should be encoded to be sent back to browser ----------------------------------------------
        # encoding to base64 is used to send ansi hebrew data. it is decoded to become string and put into json.
        # json is encoded to be sent to browser.

        if postdict["action"] == "removepass" and bool(restuple[0]):
            file64dec = []
            for eachfile in restuple:
                file64enc = base64.b64encode(eachfile)
                file64dec.append(file64enc.decode())
            #
            
            replymsg = json.dumps([file64dec[0],file64dec[1]]).encode('UTF-8')
        #
        elif postdict["action"] == "returnpass" and bool(res):
            file64enc = base64.b64encode(res)
            file64dec = file64enc.decode()
            
            replymsg = json.dumps([file64dec]).encode('UTF-8')
        #

        else: #if filesdict is empty
            replymsg = json.dumps(["Error","No file provided"]).encode('UTF-8')
        #
        
        return replymsg
    #
    
    #except Exception as e:
    #    common.errormsg(title=__name__,message=e)
    #    replymsg = json.dumps(["Error","myfunc -" + str(e)]).encode('UTF-8')
    #    return replymsg
    #
#