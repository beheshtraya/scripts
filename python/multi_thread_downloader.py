# -*- coding: cp1252 -*-

import os
import urllib
from KThread import KThread
from time import sleep
from progressbar import ProgressBar

chunk_size = 8192


class myURLOpener(urllib.FancyURLopener):
    """Create sub-class in order to override error 206.  This error means a
       partial file is being sent,
       which is ok in this case.  Do nothing with this error.
    """
    def http_error_206(self, url, fp, errcode, errmsg, headers, data=None):
        pass


def download(url, path):
    start_byte = 0
    myUrlclass = myURLOpener()
    numBytes = 0
    t = None
    first_iteration = True

    while True:
        try:
            ### Open link
            webPage = myUrlclass.open(str(url))
        except IOError, e:
            e = str(e)
            if e.__contains__('[Errno 2]'):
                ### Link doesn't have protocol, add default protocol (HTTP) to link and try again
                print ('Http protocol')
                url = 'http://' + url
                continue

            elif e.__contains__('[Errno socket error]'):
                if e.__contains__('[Errno 11001]'):
                    ### Cannot open link
                    print ('Cannot open link')
                    return

        ### Get and validate file type
        file_type = webPage.headers['Content-Type']
        if file_type.__contains__('text'):
            print ('Invalid file type, ' + file_type)
            return
    

        if first_iteration:            
            ### Get file name, if http response header contains file name get it,
            ### otherwise get file name from link                
            file_name = str()
            if webPage.headers.dict.has_key('content-disposition'):
                value = webPage.headers['Content-Disposition']
                i = value.find('filename=')
                if i != -1:
                    file_name = value[i+10:-1]

            else:
                temp = url
                i = temp.find('?')
                if i != -1:
                    temp = temp[:i]
                i = temp.rfind('/')
                file_name = temp[i+1:]
                    
            print ('File name: ' + file_name)
            path = path + '/' + file_name

        if os.path.exists(path):
            ### If the file exists, then only download the remainder
            outputFile = open(path,"ab")
            start_byte = os.path.getsize(path)
            
            ### Open link again but only request the reminder
            myUrlclass.addheader("Range", "bytes=%s-" % start_byte)
            webPage = myUrlclass.open(str(url))        
        else:
            outputFile = open(path,"wb")     


        if first_iteration:            
            ### Get file size
            try:
                size = int(webPage.headers['Content-Length']) + start_byte
                print("File size: " + str("%.2f" % (float(size) / 1024)) + " KB\n")
            except KeyError, e:
                if str(e).__contains__('content-length'):
                    size = 'Unkonwn'
                    print("Remaining size: Unknown")        

            print("Size already downloaded " + str("%.2f" % (float(start_byte) / 1024)) + " KB\n")
            
        #If the file exists, but we already have the whole thing, don't download again
        if size == start_byte:
            print("File already has been downloaded \n")
        else:
            if first_iteration:
                print("Downloading ...\n")
                t = KThread(target=progress, args=(size, path))
                t.start()
            
            numBytes = 0

            while True:
                data = webPage.read(chunk_size)
                if not data:
                        break
                outputFile.write(data)
                numBytes += len(data)

            webPage.close()
        
        outputFile.close()
        first_iteration = False

        if size >= numBytes + start_byte or size == 'Unknown':
            break

    sleep(2)
    t.kill()
    print ("\n\nDownload finish successfully\n\n------------------------------------------------------------------------------\n")
    return


def progress(size, path):
    on_disk_size = 0
    pbar = ProgressBar(maxval=size)
    pbar.start()
    while on_disk_size != size:
        on_disk_size = os.path.getsize(path)
        pbar.update(on_disk_size)
        sleep(1)
    pbar.finish()
