from serialWorker import SerialWorker
import time,random #for testing only
from util import makePGChart,makeChartData
import flask
import json
from threading import Lock

app=flask.Flask(__name__)

ds=[]
lock=Lock()
dw=DiskWriter(FILENAME,CHUNKSIZE,ds,lock,SLEEPTIME)
ds=dw.readDatastore()
dw.start()
sw=SerialWorker(None,ds,lock)

@app.route("/dayInMinutes.svg")
def minutes():
  chart=makePGChart(time.time()-24*60*60,60,ds)
  return chart.render_response()

#currently a hack
@app.route("/<length>/<interval>")
def lenInt(length,interval):
  chart=makePGChart(time.time()-int(length),int(interval),ds)
  return chart.render_response()

#currently a hack
@app.route("/data/<length>/<interval>")
def data(length,interval):
  return flask.Response(json.dumps(makeChartData(time.time()-int(length),int(interval),ds)),mimetype='application/json')
  
app.run(host='0.0.0.0',port=8080)
