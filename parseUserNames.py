import numpy as np
import urllib
import simplejson
import time
from datetime import datetime
import pandas
from scipy import stats as S


'''
url = "http://reporobot.jlord.us/data"
urllib.urlretrieve(url, filename="usernames.json")
'''

rootdir = "/home/ubuntu/github/patchwork/"

dic = simplejson.loads(open(rootdir + "usernames.json",'rb').read())
#df2015 = pandas.io.parsers.read_csv("results-20150721-150046.csv")

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



def exportUserNames(outdic,subsample=0.05):
    users = np.array(outdic['userList'])

    index = np.random.randint(0,len(users),int(subsample*len(users)))
    
    f =open("users.txt",'wb')
    for u in users[index]:
        f.write("'" + u + "'")
        f.write(",")


def build_main_df(sampling_resol="1D"):
    '''
    Main DataFrame (df): 
    This pandas dataframe contains all timestamped events related to users 
    identified as having taken part to AstroWeek 2014. Repositories related 
    to events are also provided
    '''
    
    
    #Parse .csv files and create a timestamp column to merge 2014 and 2015 datasets
    df2014 = pandas.io.parsers.read_csv(rootdir+"events_2014.csv")
    df2014['timestamp'] = np.array([datetime.strptime(dt,"%Y-%m-%d %H:%M:%S") for dt in df2014['created_at']])
    
    df2014.rename(columns={'actor_attributes_login':'actor'}, inplace=True)
    df2014.rename(columns={'repository_name':'repo'}, inplace=True)
    df2014.rename(columns={'repository_url':'repo_url'}, inplace=True)
    df2014.rename(columns={'repository_created_at':'repo_created_at'}, inplace=True)
    
    df2015 = pandas.io.parsers.read_csv(rootdir+"events_2015.csv")
    df2015['timestamp'] = map(datetime.fromtimestamp,df2015['created_at'])
    
    df2015.rename(columns={'actor_login':'actor'}, inplace=True)
    df2015.rename(columns={'repo_name':'repo'}, inplace=True)
    
    df = pandas.concat([df2014,df2015])
    df.index = df['timestamp']
    #df2014['repo_created_at'] = np.array([datetime.strptime(dt,"%Y-%m-%d %H:%M:%S") for dt in df2014['repo_created_at']])
    
    t_resol = sampling_resol
    
    event_types = np.unique(df.type.values)
    event_dic = {}
    event_dic['all'] = df.type.resample(t_resol,how='count')
    event_count = df.type.resample(t_resol,how='count')
    
    for e in event_types:
        event_dic[e] = df[df['type']==e].type.resample(t_resol,how='count')
    
        if len(event_dic[e]) < len(event_count):
            event_dic[e] = fill_ommitted_resample(event_dic[e],event_count)
        
        #print e,len(event_dic[e])
    
    
    resampled = {"activity" : 
                    {'events' : event_count,
                     'actors' : df.actor.resample(t_resol,how=countUnique),
                     'repos' : df.repo.resample(t_resol,how=countUnique)
                     },
                 'event_types' : event_dic
                }


    return df,df2014,df2015,resampled

def countUnique(array):
    return len(set(array))

def fill_ommitted_resample(df,ref_df):
    
    i=0
    while ref_df.index[i] < df.index[0]:
        #print i , ref_df.index[i],df.index[0] , ref_df.index[i] < df.index[0]
        df = df.set_value(ref_df.index[i], 0)
        i+=1
    
    df = df.sort_index()


    i=-1
    while ref_df.index[i] > df.index[i]:
        #print i,ref_df.index[-i] > df.index[-1]
        df = df.set_value(ref_df.index[i], 0)
        i-=1
    
    df = df.sort_index()
    
    return df


if __name__ == '__main__':
    print "blah"