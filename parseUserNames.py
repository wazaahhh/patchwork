import numpy as np
import urllib
import simplejson
import time
from datetime import datetime
'''
url = "http://reporobot.jlord.us/data"
urllib.urlretrieve(url, filename="usernames.json")
'''

rootdir = "/home/ubuntu/github/patchwork/"

dic = simplejson.loads(open(rootdir + "usernames.json",'rb').read())


def parseUsers(save=True):
    userList = []
    timeList = []
    timestampList = []
    prNumList = []
    
    for i,ix in enumerate(dic):
        
        if ix.has_key("username"):
            userList.append(ix['username'])
        elif ix.has_key("user"):
            userList.append(ix['user'])
            
        timeList.append(ix['time'])
        timestampList.append(time.mktime(datetime.strptime(ix['time'],'%Y-%m-%dT%H:%M:%SZ').timetuple()))
        prNumList.append(ix['prNum'])


    output = {'userList' : userList,
              'timeList': timeList,
              'prNumList' : prNumList,
              'timestampList' : timestampList
              }

    if save:
        outfile = open(rootdir + "userList.json", 'wb').write(simplejson.dumps(output))
        
    return output

