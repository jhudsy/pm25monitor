from threading import Thread
import csv,time

class DiskWriter(Thread)
  def __init__(filename,chunksize,datastore,lock,sleeptime):
    self.datastore=datastore
    self.lock=lock
    self.filename=filename
    self.chunksize=chunksize
    self.sleeptime=sleeptime
    self.lastwrite=0 #last written element

  def readDatastore()
    self.lock.acquire()
    with open(self.filename,"rb+") as f:
        csvreader=csv.reader(csvfile)
        for row in csvreader:
                self.datastore.append([long(row[0]),float(row[1]),float(row[2])])
    self.lastwrite=len(self.datastore)
    self.lock.release() 
    return self.datastore

  def run(self):
    while True:
            time.sleep(self.sleeptime)
            self.lock.acquire()
            if len(self.datastore)>=self.lastwrite+self.chunksize:
                with open(self.filename,"ab+") as f:
                    csvwriter=csv.writer(csvfile)
                    for d in self.datastore[lastwrite:]:
                            csvwriter.writerow(d)
                self.laswrite=len(self.datastore)
            self.lock.release() 
              
