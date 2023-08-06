class data_model:
    import requests
    
    doc={"filename":"","fingerprint":"","process":""}
    server="http://neuron4web.palermo.enea.it"
    path="data"
    rev=""
    fn=""
    uri="{0}/{1}".format(server,path)
    updateuri="{0}/update/".format(server)
    
    def __init__(self,did,pid,fn=""):
        if fn:
            self.doc['filename']=fn
            self.doc['process']=pid
            self.did=did
    
    def updatedata(self):
        res=requests.post("{0}/{1}".format(self.updateuri,self.did),json=self.doc)
        return res


