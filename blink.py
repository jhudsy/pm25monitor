import redis,blinkt

__PM25='sensor1pm25'
__PM10='sensor1pm10'

"""http://apps.who.int/iris/bitstream/10665/69477/1/WHO_SDE_PHE_OEH_06.02_eng.pdf"""

__PM25GREEN=10
__PM25YELLOW=18
__PM10GREEN=20
__PM10YELLOW=50

__PM25PIXEL=0
__PM10PIXEL=7

def updateBlink(channel,value):
  if channel==__PM25:
    if value<__PM25GREEN:
      blinkt.set_pixel(__PM25PIXEL,0,255,0,0.05)
    elif value<__PM25YELLOW:
      blinkt.set_pixel(__PM25PIXEL,255,60,0,0.3)
    else:
      blinkt.set_pixel(__PM25PIXEL,255,0,0,0.5)
  else:
    if value<__PM10GREEN:
      blinkt.set_pixel(__PM10PIXEL,0,255,0,0.05)
    elif value<__PM25YELLOW:
      blinkt.set_pixel(__PM10PIXEL,255,60,0,0.3)
    else:
      blinkt.set_pixel(__PM10PIXEL,255,255,0,0.5)
  blinkt.show()

r=redis.StrictRedis(host='localhost', port=6379,db=0)
p = r.pubsub(ignore_subscribe_messages=True)
p.subscribe(__PM25)
p.subscribe(__PM10)

while True:
  for message in p.listen():
    updateBlink(message['channel'],float(message['data']))
