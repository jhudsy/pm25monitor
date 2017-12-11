import serial,time#,datetime
from bisect import bisect_left

class serialWorker(Thread):
  def __init__(self,port,datastore,lock):
    Thread.__init__(self)
    if port==None:
      port="/dev/ttyUSB0"
    self.s=serial.Serial(port)
    self.datastore=datastore
    self.lock=lock
    self.start()

  def readInt(self):
    return int(self.s.read().encode('hex'),16)

  def readPM25PM10(self):
    b=self.readInt()
    while b!=0xaa:
       b=self.readInt()
    
    pm25l=self.readInt()
    pm25h=self.readInt()
    pm10l=self.readInt()
    pm10h=self.readInt()
    i1=self.readInt()
    i2=self.readInt()
    cs=self.readInt()
    checksum=(pm25l+pm25h+pm10l+pm10h+i1+i2)%256
    if cs==checksum:
      return [ float(pm25h*256+pm25l)/10,  float(pm10h*256+pm10l)/10 ]
    return None

  def run(self):
    while True:
      t=self.readPM25PM10()
      if t!=None:
        [p25,p10]=t
        d=round(time.time())
        self.lock.acquire()
        self.datastore.append([d,p25,p10])
        self.lock.release()
      time.sleep(1)

#returns a chart starting at startTime till the current time, with averages of timesize duration, e.g., starttime could be now-60 minutes, timesize could be 1 minute should return a minute average for the last hour
def getChart(startTime,timesize,datastore):
  while True:
    s0=0.0
    s1=0.0
    startIndex=bisect_left(datastore,startTime)
    endIndex=bisect_left(datastore,startTime+timesize)
    if startIndex==endIndex:
      break
    for i in range(startIndex,endIndex):
      s0+=datastore[i][1]
      s1+=datastore[i][2]
    s0/=(endIndex-startIndex+1)
    s1/=(endIndex-startIndex+1)




#      print datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"), \
