import gzip
import simplejson
import numpy as np
from dateutil import parser


data2014 = "/home/ubuntu/github/patchwork/data/patchwork_biggoogle_queries_2014_output.json.gz"
data2015 = "/home/ubuntu/github/patchwork/data/patchwork_biggoogle_queries_2015_output.json.gz"

dateEvents = ['January 29, 2014', 'March 27th, 2014','June 19, 2014','July 10, 2014','August 14, 2014','September 18, 2014','September 30, 2014',
              'October 9, 2014','October 14, 2014','October 20, 2014','October 23, 2014','October 29, 2014','November 5, 2014','November 24, 2014',
              'December 10, 2014','February 2, 2015','February 4, 2015','March 12, 2015','April 13, 2015','April 14, 2015','May 20, 2015',
              'May 21, 2015','May 28, 2015','June 23, 2015','August 18, 2015']

for d,date in enumerate(dateEvents):
    dateEvents[d] = parser.parse(date)


def rankorder(x):
   x1 = list(np.sort(x))
   x1.reverse()
   y1 = range(1,len(x1)+1)
   return np.array(x1),np.array(y1)

def parseLine(line):
    
    if line.has_key('actor_attributes_login'):
        try:
            line['repo_name'] = line.pop('repository_name')
            line['repo_url'] = line.pop('repository_url')
            line.pop('repository_created_at')
        except:
            pass
        
        line['actor_login'] = line.pop('actor_attributes_login')
        
    return line


def parseFile(path):
    with gzip.open(path) as f:
        for l,line in enumerate(f):
            line =  parseLine(simplejson.loads(line))
            print line.keys()
            
            if l==10:
                return line
            
            
def makeEventList():
    eventList = []
    userList = []
    dateList = []
    for path in [data2014,data2015]:
        with gzip.open(path) as f:
            for l,line in enumerate(f):
                line = simplejson.loads(line)
                line =  parseLine(line)
                #try:
                #    line =  parseLine(line)
                #except:
                #    print l,line['type'] 
                
                try:
                    eventList.append(line['type'])
                    userList.append(line['actor_login'])
                    dateList.append(parser.parse(line['created_at']))
                except:
                    print line
                    break
                
    return {'type': eventList, 'user': userList, 'date':dateList}


def eventsPerUserCDF(dic):
    uusers = np.unique(dic['user'])
    users = np.array(dic['user'])
    events = []
    
    for u in uusers:
        events.append(len(users[users==u]))
        
    return {'unique_users': uusers, 'events': events}