class log:
    
    def __init__(self,pid,did):
        self.processid=pid
        self.dataid=did
        self.fout="/tmp/{0}.log".format(pid)
        print self.fout
        with open(self.fout,'w') as f:
            f.write("processid: {0} -- dataid: {1} \n".format(pid,did))
            
    def out(self,string):
        with open(self.fout,'a') as f: 
            f.write("{0}: {1}\n".format(datetime.now().isoformat(),string))
    

