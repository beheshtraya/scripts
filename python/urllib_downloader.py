# -*- coding: cp1252 -*-

import os
import urllib
from time import sleep

chunk_size = 8192


class myURLOpener(urllib.FancyURLopener):
    """Create sub-class in order to override error 206.  This error means a
       partial file is being sent,
       which is ok in this case.  Do nothing with this error.
    """
    def http_error_206(self, url, fp, errcode, errmsg, headers, data=None):
        pass

    
def download(link, outputFile, start_byte=0):
        
    myUrlclass = myURLOpener()
    if start_byte != 0:
        #If the file exists, then only download the remainder
        myUrlclass.addheader("Range", "bytes=%s-" % start_byte)
        
##    try:
    webPage = myUrlclass.open(str(link))
    size = int(webPage.headers['Content-Length'])
    print("\n")
    print("File size: " + str("%.2f" % (float(size) / (1024 * 1024))) + " MB\n")
    print("Size already downloaded " + str("%.2f" % (float(start_byte) / (1024 * 1024))) + " MB\n")
    #If the file exists, but we already have the whole thing, don't download again
    if size == start_byte:
        print("File already has been downloaded \n")

##    except:
##        return "Error on opening link"

    try:
        print("Downloading ...\n")
        numBytes = 0

        while True:
            data = webPage.read(chunk_size)
            if not data:
                break
            outputFile.write(data)
            numBytes += len(data)

        webPage.close()

    except:
        return "Error"


def prepare_download(link, path):
    url = link
    existSize = 0
    dlFile = path
    if os.path.exists(dlFile):
        outputFile = open(dlFile,"ab")
        existSize = os.path.getsize(dlFile)
    else:
        outputFile = open(dlFile,"wb")

    print 'yes'
    result = download(url, outputFile, existSize)
    print 'finish prepare'
    outputFile.close()
     
    return "Download finish successful"


