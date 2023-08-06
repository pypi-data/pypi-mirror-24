from datetime import datetime
import time,calendar,requests,re

def datetotimestamp(datestr):
    """Convert date string to timestamp.
    Arguments: date string format YYYY-MM-DD"""
    try:
        y,m,d=datestr.split('-')
        return calendar.timegm(datetime(int(y),int(m),int(d)).timetuple())
    except Exception as e:
        print e
        print "wrong date format, use yyyy-mm-dd"
        return None

def getfileforid(idx,destfolder):
    """Get an index from database to local folder.
    Arguments: index of file in db, string to destination folder
    Return True if file correctly downloaded, False otherwise.
    """

    procid = processobj.requestwavefile(idx)
    if (procid!=None):
        count = 10
        fr = processobj.checkforfileready()
        while (count > 0) and (len(fr)==0):
            count = count - 1
            fr = processobj.checkforfileready()
            time.sleep(10)
        if len(fr)>0:
            idx,fwav=fr[0]
            print 'file {0} ready\n'.format(fwav)
            url = "{0}/{1}/{2}".format(processobj.uri,idx,fwav)
            print "GET {0}".format(url)
            doc = requests.get("{0}/{1}".format(processobj.uri,idx))
            get = requests.get("{0}".format(url),stream=True)
            with open("{0}/{1}".format(destfolder,fwav),"wb") as fout:
                for chunck in get.iter_content(1024):
                    fout.write(chunck)
            print "file ready!"
            
            ## delete from db ###
            res = requests.delete("{0}".format(url),headers={'If-Match':doc.json()['_rev']})
            return True
        else:
            print "timeout on upload\n"
    else:
        print "unable to create request"
    return False

def listfordate(startstr,endstr):
    """Get catalog of files in database, ordered by deceremental order of date range from input.
    If invalid or none passend, get first 100 files.
    
    Arguments: startstr a date string format YYYY-MM-DD for start range, endstr a date string format YYYY-MM-DD for end range.
    Return an Array of ids of file in database or []"""
    server = "http://neuron4web.palermo.enea.it"
    db = "data"
    API = "_design/data/_list/files/bydate"
    query = "order=true&format=json&stale=update_after"
    ra = {'startkey':datetotimestamp(startstr),'endkey':datetotimestamp(endstr)}
    if (ra['startkey'] != None) and (ra['endkey'] != None):
        query+="&startkey="+str(ra['startkey']*1000)+"&endkey="+str(ra['endkey']*1000)
    else:
        query+="&limit=100"
    url = server+"/"+db+"/"+API+"?"+query
    print url
    res=requests.get(url)
    if (res.status_code==200):
        result=res.json()['result']
        return [doc['id'] for doc in result]
    return None
