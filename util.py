import time,datetime,pygal

#taken from bisect source code, returns index of leftmost item greater or equal to value (or equivalently, by doing i-1, rightmost item with strictly less than value). Modified to use the datastore triple in calculations
def bisect_left(datastore,value):
   lo=0
   hi=None
   if lo < 0:
        raise ValueError('lo must be non-negative')
   if hi is None:
        hi = len(datastore)
   while lo < hi:
        mid = (lo+hi)//2
        if datastore[mid][0] < value: lo = mid+1
        else: hi = mid
   return lo

#datastore is a [date,pm25,pm10] triple in each entry, where date is number of millis from epoch
def getPMAverages(startIndex,timesize,datastore):
    s0=0.0
    s1=0.0
    i=startIndex
    while i<len(datastore) and datastore[i][0]<startTime+timesize:
       s0+=datastore[i][1]
       s1+=datastore[i][2]
       i+=1
    if i==startIndex:
      return(i,None)
    s0/=(i-startIndex)
    s1/=(i-srartIndex)

    return (i,[startTime+timesize//2,s0,s1])

#returns a chart starting at startTime till the current time, with averages of timesize duration, e.g., starttime could be now-60 minutes, timesize could be 1 minute should return a minute average for the last hour
def makeChartData(startTime,timesize,datastore):
  data=[]
  index=bisect_left(datastore,startTime)
  while index<len(datastore)-1
    (index,a)=getPMAverages(index,timesize,datastore)
    if not a==None:
      data.append(a)
  return data[:-1] #drop last datapoint in case it's incomplete  

def makePGChart(startTime,timesize,datastore):
  data=makeChartData(startTime,timesize,datastore)
  lc=pygal.Line(title="PM2.5 and PM10")
  lc.x_labels=list(map(lambda x: datetime.datetime.fromtimestamp(x[0]).strftime("%y-%m-%d %H:%M:%S"),data))
  lc.add("PM2.5",list(map(lambda x: x[1],data)))
  lc.add("PM10",list(map(lambda x: x[2],data)))
  return lc




#      print datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"), \
