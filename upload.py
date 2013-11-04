#!/usr/bin/env python3

"""
The purpose of this script is to make the current status of solar
panels as reported by a SMA Sunny WebBox available online without
exposing its Web front-end (with the login form) to the users.

Additional benefits are that the web front-end can collect all
individual measurements of the box in a database and provide a more
feature-rich visualization.

Note: Retrieving data from the WebBox does _not_ require a login.

"""

import sys
import os
sys.path.append(os.getenv('HOME') + '/bin/')

import re
import time
import requests

# --------------------------------------------------
# Configuration
BASEURL='http://somehost/somedirectory'
USER='abcd'
PASSWORD='123456'

SUNNY='http://webboxip'
WAIT=10

# --------------------------------------------------
# Some helper functions
PUTURL='%s/putData.php' % BASEURL
GETURL='%s/home.ajax' % SUNNY

POWER='Power'
DAILY='DailyYield'
TOTAL='TotalYield'

UNITPREFIX={ 'k': 1000, 'M': 1000*1000, 'G': 1000*1000*1000 }

def decode_number(num):
    """
    Parse number as returned from Sunny WebBox.

    Assumes the given number is in English. Uses UINTPREFIX to parse
    a potential prefix of the unit given and convert the number to a float.

    """
    r = re.match('^([0-9.]+)[ ]+([kM]?)(Wh|W)?$', num)
    if r:
        factor = UNITPREFIX.get(r.group(2), 1)
        return float(r.group(1))*factor
    else:
        raise Exception('Cannot parse number [%s]' % num)


def decode_json(json):
    """
    Extract measurement from json.

    """
    power = None
    daily = None
    total = None

    i = json['Items']

    for e in i:

        if POWER in e:
            power = decode_number(e[POWER])
        if DAILY in e:
            daily = decode_number(e[DAILY])
        if TOTAL in e:
            total = decode_number(e[TOTAL])

    return (power, daily, total)
    

def put(power, daily, total):
    """
    Upload data to webpage.

    """
    data = {
        'currPower': power, 
        'dailyEnergy': daily,
        'wholeEnergy': total
        }
    try:
        r = requests.post(PUTURL, data=data, auth=(USER, PASSWORD))
        print(r.text)
    except:
        print("put() failed, continuing")


def get():
    """
    Request current status from Sunny WebBox

    We set the language for the request to English. This ensures that
    we can parse the returned values.

    """
    try:
        r = requests.post(GETURL, headers={'AcceptLanguage': 'en,en-gb;q=0.7,de-de;q=0.3'})
        j = r.json

        return decode_json(j)
    except:
        print("get() failed, continuing")
    

def run():
    """
    Runs the program logic
    
    """
    while True:
        r = get()

        if r:
            (power, daily, total) = r
            put(power, daily, total)

            print('%s %s %s' % (power, daily, total))

        time.sleep(WAIT)
            
if __name__ == "__main__":
    run()
