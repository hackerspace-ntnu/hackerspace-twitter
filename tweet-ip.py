#!/usr/bin/env python2

import subprocess
import time
import urllib2
import sys
from random import randint

from twitter import Twitter, OAuth, TwitterError
from secret import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_SECRET, CONSUMER_KEY


TIMEOUT = 5


def is_internet_on():
    """Check if we have a connection to twitter.com"""
    try:
        urllib2.urlopen('http://twitter.com', timeout=1)
        return True
    except urllib2.URLError:
        pass
    return False


def get_serial():
    """Extract serial from cpuinfo file"""
    try:
        with open('/proc/cpuinfo', 'r') as open_file:
            for line in open_file:
                if line.startswith('Serial'):
                    return line[10:26]
    except:
        return "ERROR000000000"

    return "0000000000000000"


def get_ip():
    p = subprocess.Popen('ip route list', shell=True, stdout=subprocess.PIPE)
    data = p.communicate()
    split_data = data[0].split()
    return split_data[split_data.index('src') + 1]


try:
    while not is_internet_on():
        print "No internet connection detected, trying again in {}s".format(TIMEOUT)
        time.sleep(TIMEOUT)

    print "Internet connection detected!"
    rng = randint(1, 999)
    ip = get_ip()
    serial = get_serial()

    while True:
        try:
            twitter = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
            print "Authed with twitter!"

            status = '<%d>(%s) piip: %s' % (rng, serial, ip)
            print status

            twitter.statuses.update(status=status)
            print "Tweeted!"
            break
        except TwitterError:
            print "TwitterError!! Trying again in {}s".format(TIMEOUT)
            time.sleep(TIMEOUT)
            continue

except KeyboardInterrupt:
    print "Stopping tweet-ip.py"
    sys.exit()
