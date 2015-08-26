import os
import re
import numpy as np
from dateutil import parser
from datetime import datetime


eventDir = "/home/ubuntu/github/patchwork/data/events/"
eventFiles = os.listdir(eventDir)


def parseUsers():
    userDic = {}
    pwDates = []
    for e,ex in enumerate(eventFiles):
        #print e,ex
        
        eventPlace = re.findall("--(.*?)-",ex)[0]
        eventDate = re.findall("-(\d.*?).csv",ex)[0]
        #print eventPlace,eventDate
        date = parser.parse(eventDate)
        pwDates.append(date)
        
        with open(eventDir + ex) as f:
            file = f.read()
            file = file.split("\n")
            
            for line in file:
    
                line = line.split(",")
    
                if line == ['']:
                    continue
                
    
                
                try:
                    userDic[line[0]][eventPlace].append(eventPlace)
                    userDic[line[0]][date].append(date)
                except:
                    userDic[line[0]] = {'jDate' : parser.parse(line[1]), 'pwPlace' : [eventPlace], 'pwDate' : [date]}
    
    return userDic,np.sort(pwDates)