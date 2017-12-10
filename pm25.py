import serial,time,datetime
s=serial.Serial('/dev/ttyUSB0')

while True:
  b=s.read(20)
  for i in range(len(b)):
    x=int(b[i].encode('hex'),16)
    if x==0xaa: #found header
       break

  #get values
  pm25l=int(b[i+2].encode('hex'),16)
  pm25h=int(b[i+3].encode('hex'),16)
  pm10l=int(b[i+4].encode('hex'),16)
  pm10h=int(b[i+5].encode('hex'),16)
  i1=int(b[i+6].encode('hex'),16)
  i2=int(b[i+7].encode('hex'),16)
  cs=int(b[i+8].encode('hex'),16)
  checksum=(pm25l+pm25h+pm10l+pm10h+i1+i2)%256
  if cs==checksum:
    print datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"), \
          float(pm25h*256+pm25l)/10, \
          float(pm10h*256+pm10l)/10

  time.sleep(1)
