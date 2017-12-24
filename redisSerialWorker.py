import serial,time,redis
import numpy as np

"""store readings every minute"""
__SAMPLINGINTERVAL=60
"""serial port device from which to read"""
__PORT="/dev/ttyUSB0"
__serialport=serial.Serial(__PORT)
"""redis key for sorted set"""
__SSKEY="sensor1ts" 
"""redis key for current reading"""
__KEY="sensor1Current"
"""channels for pubsub"""
__PM25="sensor1pm25"
__PM10="sensor1pm10"

def readInt():
    i = int(__serialport.read().encode('hex'),16)
    return i

  #NB: return is p2.5,p10
def readPM25PM10():
    b=readInt()
    while b!=0xaa:
       b=readInt()
    readInt() #read dummy
    pm25l=readInt()
    pm25h=readInt()
    pm10l=readInt()
    pm10h=readInt()
    i1=readInt()
    i2=readInt()
    cs=readInt()
    checksum=(pm25l+pm25h+pm10l+pm10h+i1+i2)%256
    if cs==checksum:
      return [ (pm25h*256+pm25l)/10,  (pm10h*256+pm10l)/10 ]
    return None

#####################################
r = redis.StrictRedis(host='localhost', port=6379, db=0)
pubsub=r.pubsub()

lastwrite=round(time.time()) #time last reading was stored
readings=[] #the readings
while True:
      t=readPM25PM10()
      d=round(time.time())
      if t!=None:
        readings.append(t)      
        r.set(__KEY,t)
        r.publish(__PM25,t[0])
        r.publish(__PM10,t[1])
      if d-lastwrite>=__SAMPLINGINTERVAL:
              lastwrite=d
              toRedis=(np.sum(readings,axis=0)/len(readings)).tolist()
              toRedis.append(int(d))
              r.zadd(__SSKEY,int(d-(__SAMPLINGINTERVAL)//2),toRedis)
              readings=[]
      time.sleep(1)
