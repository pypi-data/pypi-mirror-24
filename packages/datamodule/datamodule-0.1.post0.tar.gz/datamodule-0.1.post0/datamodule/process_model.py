class process_model:
    import requests
    
    waverequestdoc={"format":"","executable":"","params":""}
    server="http://neuron4web.palermo.enea.it"
    path="data"
    rev=""
    fn=""
    uri="{0}/{1}".format(server,path)
    
    def __init__(self,executable="test.exe",params="-test",fmt="wave"):
        self.waverequestdoc['format']=fmt
        self.waverequestdoc['executable']=executable
        self.waverequestdoc['params']=params
    
    def updatedata(self,idx):
        if 'request' in self.waverequestdoc:
            del self.waverequestdoc['request']
        res=requests.post("{0}/processupdate/{1}".format(self.server,idx),json=self.waverequestdoc)
        if res.status_code==200:
            self.rev=res.headers['X-Couch-Update-NewRev']
            return True
        return False
        
    def getdata(self,idx):
        res=requests.get("{0}/{1}".format(self.uri,idx))
        if res.status_code==200:
            return res.json()
        else:
            return None
    
    def getido(self,id):
        data=self.getdata(idx)
        if data:
            return data['head_iadp']['ido']
        else:
            return None
    
    def getids(self,idx):
        data=self.getdata(idx)
        if data:
            return data['head_iadp']['ids']
        else:
            return None
    
    def getidh(self,idx):
        data=self.getdata(idx)
        if data:
            return data['head_iadp']['idh']
        else:
            return None
    
    def getfilename(self,idx):
        data=self.getdata(idx)
        if data:
            if 'filename' in data:
                return data['filename']
        return None
    
    def getfilesready(self):
        res=requests.get("{0}/fileready".format(self.server),headers={'Accept':'application/json'})
        if res.status_code==200:
            return res.json()['result']
        return None
    
    def isfileready(self,fn):
        obj=self.getfilesready()
        return [(o['id'],o['value'].keys().pop()) for o in obj if o['value'].keys().pop()==fn]
    
    def checkforfileready(self):
        return self.isfileready("{0}.wav".format(self.fn.split('.')[0]))
        
        #test=[(i,fn) for k,v in obj if ]
    def requestwavefile(self,idx):
        self.fn=self.getfilename(idx)
        ret=None
        if self.fn:
            testarray=self.checkforfileready()
            if len(testarray)>0: 
                obj=self.getdata(testarray.pop()[0])
                self.rev=obj['_rev']
                ret=obj['_id']
            else:
                self.waverequestdoc['request']=self.fn
                res=requests.post("{0}".format(self.uri),json=self.waverequestdoc)
                if res.status_code==201: 
                    obj=res.json()
                    self.rev=obj['rev']
                    ret=obj['id']
        return ret

