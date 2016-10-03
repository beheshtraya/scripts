"""
    beheshtraya file downloader (bfd)
    written by Seyed Mohammad Javad Beheshtian
    beheshtraya@gmail.com

    description: This module uses pycurl for fetching urls
    and tested in python 2.7.6 & 2.7.7 but it may work in other
    python versions.

    you can download pycurl from http://pycurl.sourceforge.net/download

    license: The MIT License (MIT)

    Copyright (c) 2014 beheshtraya

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
    
"""
    
from cStringIO import StringIO
from time import sleep
from os.path import exists, getsize
from urllib import unquote
import sys
try:
    from pycurl import Curl, error as curlError
except ImportError:
    print 'pycurl not installed.'
    print 'You can download it from http://pycurl.sourceforge.net/download'
    sys.exit(0)

def download(url, path, proxy='', cookie='', timeout=60,
             low_speed_time=20, low_speed_limit=10240,
             not_alowed_types=['text']):
    
    c = Curl()
    header = StringIO()

    c.setopt(c.URL, url)
    c.setopt(c.NOBODY, True)
    c.setopt(c.PROXY, proxy)
    c.setopt(c.HEADERFUNCTION, header.write)
    c.setopt(c.VERBOSE, False)
    c.setopt(c.NOPROGRESS, True)
    c.setopt(c.FAILONERROR, True)
    c.setopt(c.WRITEDATA, header)
    c.setopt(c.COOKIE, cookie)
    c.setopt(c.TIMEOUT, timeout)
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.USERAGENT, 'Mozilla/5.0 (Windows NT 6.3; WOW64)AppleWebKit/537.36\
                        (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36')

    while True:
        try:
            c.perform()
            break
        except curlError, error:
            errno, errstr = error
            print '\nAn error occurred: ', errno, '\n' ,errstr
            print '\n ----------------------------------------------------------------------- \n\n\n\n',
            sleep(30)    #################### temp #########################

    
    header = header.getvalue()

    filename = get_filename(header, url)
    filetype = get_filetype(filename)

    if path != '':
        filename = path + '/' + filename

    start_byte = 0
    if exists(filename):
        start_byte = getsize(filename)

    effective_url = c.getinfo(c.EFFECTIVE_URL)
    content_type = c.getinfo(c.CONTENT_TYPE)
    http_code = c.getinfo(c.HTTP_CODE)
    redirect_count = c.getinfo(c.REDIRECT_COUNT)
    content_length = c.getinfo(c.CONTENT_LENGTH_DOWNLOAD)

    for i in not_alowed_types:
        if content_type.__contains__(i):
            print 'Error: Invalid file type'
            return
    
    print 'File name: ', filename
    print 'MIME type: ', content_type
    print 'File type: ', filetype
    print 'File Size: ', int(content_length)/1024, 'KB'

    if content_length == start_byte:
        print ('\nFile already downloaded completely\n')
        print ' ----------------------------------------------------------------------- \n\n\n\n',
        return
    
    print '\nDownload start ... \n\n'

    
    c = Curl()
    c.setopt(c.URL, url)
    c.setopt(c.NOBODY, False)
    c.setopt(c.PROXY, proxy)
    c.setopt(c.VERBOSE, False)
    c.setopt(c.NOPROGRESS, False)
    c.setopt(c.FAILONERROR, True)
    c.setopt(c.COOKIE, cookie)
    c.setopt(c.LOW_SPEED_TIME, low_speed_time)
    c.setopt(c.LOW_SPEED_LIMIT, low_speed_limit)
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.USERAGENT, 'Mozilla/5.0 (Windows NT 6.3; WOW64)AppleWebKit/537.36\
                        (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36')

    
    c.setopt(c.RESUME_FROM, start_byte)

    while True:
        try:
            f = open(filename, 'ab')
            c.setopt(c.WRITEDATA, f)
            c.perform()
            f.close()
            break
        except curlError, error:
            f.close()
            errno, errstr = error
            print '\nAn error occurred: ', errno, '\n' ,errstr
            print '\n ----------------------------------------------------------------------- \n\n\n\n',
            start_byte = getsize(filename)
            c.setopt(c.RESUME_FROM, start_byte)
            sleep(30)

    
    total_time = c.getinfo(c.TOTAL_TIME)
    print 'Total time: ', total_time, ' s'


def get_filename(header, url):
    i = header.find('Content-Disposition')
    j = header.find('filename=')
    if i >= 0 and j >= 0:
        ### Http Response contains file name
        filename = header[j+10:]
        i = filename.find('"')
        filename = filename[:i]
    else:
        ### find filename from url
        filename = unquote(url.strip("/").split("/")[-1].strip())

    return filename


def get_filetype(filename):
    i = filename.rfind('.')
    if i >= 0:
        filetype = filename[i+1:]
    else:
        filetype = 'Unknown'

    return filetype


download('http://s6.p30download.com/users/606/tutorial/graphic-design/\
others/Lynda.Foundations.Of.Color.Full_p30download.com.part1.rar', '')

download('http://s6.p30download.com/users/606/tutorial/graphic-design/\
others/Lynda.Foundations.Of.Color.Full_p30download.com.part2.rar', '')

download('http://s6.p30download.com/users/606/tutorial/graphic-design/\
others/Lynda.Foundations.Of.Color.Full_p30download.com.part3.rar', '')

download('http://s1.p30download.com/users/101/audio/instrumental/\
Modern.Talking.Instrumental_p30download.com.rar', '')

download('http://s6.p30download.com/users/606/tutorial/office/\
business/Lynda.Balancing.Work.And.Life_p30download.com.rar', '')

download('http://s6.p30download.com/users/606/tutorial/\
development-web/bootstrap/Lynda.Bootstrap.3.Advanced.Web.Development_p30download.com.rar', '')

download('http://s6.p30download.com/users/606/tutorial/\
development-web/bootstrap/Lynda.Bootstrap.3.Advanced.Web.Development.Exercise.Files_p30download.com.part1.rar', '')

download('http://s6.p30download.com/users/606/tutorial/\
development-web/bootstrap/Lynda.Bootstrap.3.Advanced.Web.Development.Exercise.Files_p30download.com.part2.rar', '')

download('http://s6.p30download.com/users/606/tutorial/\
development-web/bootstrap/Lynda.Bootstrap.3.Advanced.Web.Development.Exercise.Files_p30download.com.part3.rar', '')

download('http://s6.p30download.com/users/606/tutorial/\
development-web/bootstrap/Lynda.Bootstrap.3.Advanced.Web.Development.Exercise.Files_p30download.com.part4.rar', '')

download('http://s6.p30download.com/users/606/tutorial/\
development-web/bootstrap/Lynda.Bootstrap.3.Advanced.Web.Development.Exercise.Files_p30download.com.part5.rar', '')

download('http://s6.p30download.com/users/606/tutorial/\
development-web/bootstrap/Lynda.Bootstrap.3.Advanced.Web.Development.Exercise.Files_p30download.com.part6.rar', '')

download('http://s6.p30download.com/users/606/tutorial/\
development-web/bootstrap/Lynda.Bootstrap.3.Advanced.Web.Development.Exercise.Files_p30download.com.part7.rar', '')

download('http://s6.p30download.com/users/606/tutorial/\
development-web/bootstrap/Lynda.Bootstrap.3.Advanced.Web.Development.Exercise.Files_p30download.com.part8.rar', '')




##c.setopt(c.PROXY, 'socks4://5.61.34.199:23944')
##c.setopt(c.CONNECTTIMEOUT, 10)
##c.setopt(c.TIMEOUT, 10)
##    c.setopt(c.HTTPHEADER, ['Accept: text/html,application/xhtml+xml,application\
##                        /xml;q=0.9,image/webp,*/*;q=0.8'])


""" Project started at 1st June 2014 """
